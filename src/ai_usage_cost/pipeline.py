from __future__ import annotations

from collections.abc import Callable, Hashable, Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, Field

from . import privacy, store
from .aggregate import (
    STALE_INFO_DAYS,
    Report,
    SessionFlags,
    UnknownModel,
    build_report,
    facets_of,
)
from .models import CostBreakdown, CostState, PricedEvent, UsageEvent, local_day
from .pricing import RateTable, price_event, resolve_provider
from .sources import client_labels, registry
from .sources.base import TokenData, present_roots
from .trace import Capabilities, OutcomeLabel

K = TypeVar("K", bound=Hashable)

DEFAULT_DB_PATH = Path.home() / ".ai-usage-cost" / "usage.db"


class SourceInfo(BaseModel):
    id: str
    label: str
    clients: list[str] = Field(default_factory=list)
    token_data: TokenData
    path: str
    root_hint: str
    detected: bool
    files: int
    capabilities: Capabilities = Field(default_factory=Capabilities)
    experimental: bool = False


@dataclass
class Analysis:
    events: list[PricedEvent] = field(default_factory=list)
    table: RateTable = field(default_factory=RateTable.load)
    files: int = 0
    warnings: list[str] = field(default_factory=list)
    scan_warnings: list[str] = field(default_factory=list)
    sources: list[SourceInfo] = field(default_factory=list)
    session_flags: dict[tuple[str, str], tuple[bool, int, str]] = field(default_factory=dict)
    db_path: Path | None = None
    # "Today" for rate staleness; None means the real date. Injectable so tests can pin it.
    today: date | None = None

    @property
    def rates_age_days(self) -> int | None:
        return self.table.age_days(self.today)

    @property
    def client_labels(self) -> dict[str, str]:
        return client_labels()


def unknown_models(priced: Sequence[PricedEvent]) -> list[UnknownModel]:
    totals: dict[str, tuple[int, int]] = {}
    for item in priced:
        if item.state != "unpriced" or item.event.tokens is None:
            continue
        model = item.event.model or "unknown"
        tokens, count = totals.get(model, (0, 0))
        totals[model] = (tokens + item.event.tokens.total, count + 1)
    return sorted(
        (
            UnknownModel(model=model, tokens=tokens, events=events)
            for model, (tokens, events) in totals.items()
        ),
        key=lambda u: u.tokens,
        reverse=True,
    )


def _tokens_by(
    priced: Sequence[PricedEvent],
    flagged: Callable[[CostBreakdown], bool],
    key: Callable[[UsageEvent], K],
) -> dict[K, int]:
    totals: dict[K, int] = {}
    for item in priced:
        if item.state != "priced" or item.cost is None or not flagged(item.cost):
            continue
        if not item.event.model:
            continue
        volume = item.event.tokens.total if item.event.tokens else 0
        totals[key(item.event)] = totals.get(key(item.event), 0) + volume
    return totals


def estimated_models(priced: Sequence[PricedEvent]) -> dict[str, int]:
    """Model id -> token volume, for models priced from a shorter prefix's row (match kind
    `estimated`). Benign-suffix matches (dated ids, `[1m]`, ...) are not included."""
    totals = _tokens_by(priced, lambda cost: cost.estimated, lambda event: event.model or "")
    return dict(sorted(totals.items(), key=lambda entry: entry[1], reverse=True))


def tier_unpriced_models(priced: Sequence[PricedEvent]) -> dict[tuple[str, str], int]:
    """(model id, tier) -> token volume, for requests billed at the standard price because
    the row publishes no price for the tier they ran on."""
    totals = _tokens_by(
        priced,
        lambda cost: cost.tier_unpriced,
        lambda event: (event.model or "", event.tier),
    )
    return dict(sorted(totals.items(), key=lambda entry: entry[1], reverse=True))


def reported_cost_divergences(priced: Sequence[PricedEvent]) -> list[str]:
    """One message per session whose tool-reported cost and computed cost disagree by more
    than max(5% of the reported figure, $0.01). Compared only over the events carrying both
    figures, so a session the tool reported on partially is not flagged for the gap."""
    sums: dict[tuple[str, str], tuple[float, float]] = {}
    for item in priced:
        # A free (local) model computes to $0 by definition; any figure the tool reports for
        # it is not a pricing disagreement.
        if item.event.reported_cost is None or item.cost is None or item.state == "free":
            continue
        key = (item.event.source, item.event.session_id)
        reported, computed = sums.get(key, (0.0, 0.0))
        sums[key] = (reported + item.event.reported_cost, computed + item.cost.total)
    messages = []
    for (source, session_id), (reported, computed) in sums.items():
        if abs(reported - computed) > max(0.05 * reported, 0.01):
            messages.append(
                f"session {session_id}: tool-reported cost ${reported:,.4f} differs from "
                f"computed cost ${computed:,.4f} ({source})"
            )
    return messages


def _sources_of(
    roots: dict[str, list[Path]] | None, file_counts: dict[str, int]
) -> list[SourceInfo]:
    infos = []
    for source in registry().values():
        files_found = file_counts.get(source.id, 0)
        present = present_roots(source, (roots or {}).get(source.id))
        path = ", ".join(str(root) for root in present) if present else source.display_path
        infos.append(
            SourceInfo(
                id=source.id,
                label=source.label,
                clients=sorted(source.clients.values()),
                token_data=source.token_data,
                path=path,
                root_hint=source.root_hint,
                detected=files_found > 0,
                files=files_found,
                capabilities=source.capabilities,
                experimental=source.experimental,
            )
        )
    return infos


def analyze(
    db_path: Path | None = None,
    roots: dict[str, list[Path]] | None = None,
    rates_path: Path | None = None,
    *,
    rebuild: bool = False,
    today: date | None = None,
) -> Analysis:
    resolved_db_path = db_path or DEFAULT_DB_PATH
    config = privacy.load_config()
    conn = store.open_store(resolved_db_path)
    try:
        store.ingest(
            conn,
            registry().values(),
            roots,
            rebuild=rebuild,
            exclude_projects=config.exclude_projects,
            metadata_retention_days=config.metadata_retention_days,
        )
        raw_events, files, scan_warnings = store.load(conn)
        file_counts = store.file_counts(conn)
        session_flags = store.session_flags(conn)
    finally:
        conn.close()

    table = RateTable.load(rates_path)
    priced: list[PricedEvent] = []
    for event in raw_events:
        resolved = resolve_provider(event.provider, event.model, table)
        if resolved != event.provider:
            event = event.model_copy(update={"provider": resolved})
        cost, state = price_event(event, table)
        priced.append(PricedEvent(event=event, cost=cost, state=state))

    analysis = Analysis(
        events=priced,
        table=table,
        files=files,
        warnings=list(scan_warnings),
        scan_warnings=list(scan_warnings),
        sources=_sources_of(roots, file_counts),
        session_flags=session_flags,
        db_path=resolved_db_path,
        today=today,
    )
    for unknown in unknown_models(priced):
        note = table.unpriced_note(unknown.model)
        if note:
            analysis.warnings.append(f"no rate for model {unknown.model!r} -- {note}")
        else:
            analysis.warnings.append(
                f"no rate for model {unknown.model!r} ({unknown.tokens:,} tokens) -- add it to "
                "rates.json; it is excluded from the cost total, but its tokens are still counted"
            )
    for model, volume in estimated_models(priced).items():
        rate = table.lookup(model)
        parent = rate.display if rate is not None else "a shorter prefix"
        analysis.warnings.append(
            f"model {model!r} has no rates.json row of its own -- cost is estimated from the "
            f"{parent} rate ({volume:,} tokens); add a row for {model!r} to price it exactly"
        )
    for (model, tier), volume in tier_unpriced_models(priced).items():
        analysis.warnings.append(
            f"model {model!r} has no {tier} tier price in rates.json -- {volume:,} tokens were "
            "billed at the standard rate instead"
        )
    analysis.warnings.extend(reported_cost_divergences(priced))
    age = analysis.rates_age_days
    if age is not None and age > STALE_INFO_DAYS:
        analysis.warnings.append(
            f"rates.json is {age} days old (as of {table.as_of}) -- prices may have changed "
            "since; re-verify the table"
        )
    if config.content_retention_days is not None:
        analysis.warnings.append(
            "content_retention_days is set but inert: no content is persisted in this version, "
            "so there is nothing for it to expire"
        )
    return analysis


def filter_events(
    priced: Sequence[PricedEvent],
    *,
    since: date | None = None,
    until: date | None = None,
    search: str | None = None,
    states: Sequence[CostState] | None = None,
    clients: Sequence[str] | None = None,
    providers: Sequence[str] | None = None,
    models: Sequence[str] | None = None,
    projects: Sequence[str] | None = None,
    include_sidechains: bool = True,
    outcomes: Sequence[OutcomeLabel] | None = None,
    traced: bool | None = None,
    has_errors: bool | None = None,
    session_flags: SessionFlags | None = None,
) -> list[PricedEvent]:
    term = search.lower() if search else None
    return [
        item
        for item in priced
        if (since is None or local_day(item.event.timestamp) >= since)
        and (until is None or local_day(item.event.timestamp) <= until)
        and (term is None or _matches_search(item.event, term))
        and (not states or item.state in states)
        and (not clients or item.event.client in clients)
        and (not providers or item.event.provider in providers)
        and (not models or item.event.model in models)
        and (not projects or item.event.project in projects)
        and (include_sidechains or not item.event.is_sidechain)
        and _session_passes(item, outcomes, traced, has_errors, session_flags)
    ]


def _session_passes(
    item: PricedEvent,
    outcomes: Sequence[OutcomeLabel] | None,
    traced: bool | None,
    has_errors: bool | None,
    session_flags: SessionFlags | None,
) -> bool:
    if not outcomes and traced is None and has_errors is None:
        return True
    key = (item.event.source, item.event.session_id)
    is_traced, error_count, outcome = (session_flags or {}).get(key, (False, 0, "unrated"))
    return (
        (not outcomes or outcome in outcomes)
        and (traced is None or is_traced == traced)
        and (has_errors is None or (error_count > 0) == has_errors)
    )


def _matches_search(event: UsageEvent, term: str) -> bool:
    fields = (event.session_id, event.model, event.project, event.client, event.repository)
    return any(value is not None and term in value.lower() for value in fields)


def report_of(
    analysis: Analysis,
    *,
    since: date | None = None,
    until: date | None = None,
    search: str | None = None,
    states: Sequence[CostState] | None = None,
    clients: Sequence[str] | None = None,
    providers: Sequence[str] | None = None,
    models: Sequence[str] | None = None,
    projects: Sequence[str] | None = None,
    include_sidechains: bool = True,
    outcomes: Sequence[OutcomeLabel] | None = None,
    traced: bool | None = None,
    has_errors: bool | None = None,
) -> Report:
    base = filter_events(analysis.events, since=since, until=until, search=search)
    priced = filter_events(
        base,
        states=states,
        clients=clients,
        providers=providers,
        models=models,
        projects=projects,
        include_sidechains=include_sidechains,
        outcomes=outcomes,
        traced=traced,
        has_errors=has_errors,
        session_flags=analysis.session_flags,
    )
    return build_report(
        priced,
        client_labels=analysis.client_labels,
        model_label=analysis.table.display_name,
        rates_as_of=analysis.table.as_of,
        rates_age_days=analysis.rates_age_days,
        model_match=analysis.table.match_of,
        currency=analysis.table.currency,
        files_scanned=analysis.files,
        warnings=analysis.warnings,
        scan_warnings=analysis.scan_warnings,
        unknown_models=unknown_models(base),
        facets=facets_of(base, analysis.session_flags),
        session_flags=analysis.session_flags,
    )
