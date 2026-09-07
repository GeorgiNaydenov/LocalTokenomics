from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time
from pathlib import Path

from . import store
from .aggregate import Report, UnknownModel, build_report
from .models import PricedEvent
from .pricing import RateTable, price_event, resolve_provider
from .sources import client_labels, registry

DEFAULT_DB_PATH = Path.home() / ".ai-usage-cost" / "usage.db"


@dataclass
class Analysis:
    events: list[PricedEvent] = field(default_factory=list)
    table: RateTable = field(default_factory=RateTable.load)
    files: int = 0
    warnings: list[str] = field(default_factory=list)

    @property
    def client_labels(self) -> dict[str, str]:
        return client_labels()

    def unknown_models(self) -> list[UnknownModel]:
        totals: dict[str, tuple[int, int]] = {}
        for item in self.events:
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


def analyze(
    db_path: Path | None = None,
    roots: dict[str, list[Path]] | None = None,
    rates_path: Path | None = None,
    *,
    rebuild: bool = False,
) -> Analysis:
    conn = store.open_store(db_path or DEFAULT_DB_PATH)
    try:
        store.ingest(conn, registry().values(), roots, rebuild=rebuild)
        raw_events, files, scan_warnings = store.load(conn)
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

    analysis = Analysis(events=priced, table=table, files=files, warnings=list(scan_warnings))
    for unknown in analysis.unknown_models():
        analysis.warnings.append(
            f"no rate for model {unknown.model!r} ({unknown.tokens:,} tokens) -- "
            "add it to rates.json; it is excluded from all totals"
        )
    return analysis


def filter_events(
    priced: Sequence[PricedEvent],
    *,
    since: date | None = None,
    until: date | None = None,
    clients: Sequence[str] | None = None,
    providers: Sequence[str] | None = None,
    models: Sequence[str] | None = None,
    projects: Sequence[str] | None = None,
    include_sidechains: bool = True,
) -> list[PricedEvent]:
    start = _as_datetime(since, time.min)
    end = _as_datetime(until, time.max)
    return [
        item
        for item in priced
        if (start is None or item.event.timestamp >= start)
        and (end is None or item.event.timestamp <= end)
        and (not clients or item.event.client in clients)
        and (not providers or item.event.provider in providers)
        and (not models or item.event.model in models)
        and (not projects or item.event.project in projects)
        and (include_sidechains or not item.event.is_sidechain)
    ]


def report_of(analysis: Analysis, **filters: object) -> Report:
    priced = filter_events(analysis.events, **filters)  # type: ignore[arg-type]
    return build_report(
        priced,
        client_labels=analysis.client_labels,
        model_label=analysis.table.display_name,
        rates_as_of=analysis.table.as_of,
        currency=analysis.table.currency,
        files_scanned=analysis.files,
        warnings=analysis.warnings,
        unknown_models=analysis.unknown_models(),
    )


def _as_datetime(day: date | None, at: time) -> datetime | None:
    if day is None:
        return None
    return datetime.combine(day, at).replace(tzinfo=UTC)
