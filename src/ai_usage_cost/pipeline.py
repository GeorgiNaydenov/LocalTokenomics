from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time
from pathlib import Path

from pydantic import BaseModel, Field

from . import privacy, store
from .aggregate import Report, SessionFlags, UnknownModel, build_report, facets_of
from .models import CostState, PricedEvent, UsageEvent
from .pricing import RateTable, price_event, resolve_provider
from .sources import client_labels, registry
from .sources.base import TokenData, present_roots
from .trace import Capabilities, OutcomeLabel

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
            )
        )
    return infos


def analyze(
    db_path: Path | None = None,
    roots: dict[str, list[Path]] | None = None,
    rates_path: Path | None = None,
    *,
    rebuild: bool = False,
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
    )
    for unknown in unknown_models(priced):
        analysis.warnings.append(
            f"no rate for model {unknown.model!r} ({unknown.tokens:,} tokens) -- "
            "add it to rates.json; it is excluded from all totals"
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
    start = _as_datetime(since, time.min)
    end = _as_datetime(until, time.max)
    term = search.lower() if search else None
    return [
        item
        for item in priced
        if (start is None or item.event.timestamp >= start)
        and (end is None or item.event.timestamp <= end)
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
        currency=analysis.table.currency,
        files_scanned=analysis.files,
        warnings=analysis.warnings,
        scan_warnings=analysis.scan_warnings,
        unknown_models=unknown_models(base),
        facets=facets_of(base, analysis.session_flags),
        session_flags=analysis.session_flags,
    )


def _as_datetime(day: date | None, at: time) -> datetime | None:
    if day is None:
        return None
    return datetime.combine(day, at).replace(tzinfo=UTC)
