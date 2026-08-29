"""Scan -> price -> filter -> report. The one entry point the CLI and API share."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time
from pathlib import Path

from .aggregate import Report, UnknownModel, build_report
from .models import PricedEvent
from .pricing import Pricer, RateTable
from .sources import registry, scan_all


@dataclass
class Analysis:
    """Everything parsed and priced once, so filtering is cheap."""

    priced: list[PricedEvent] = field(default_factory=list)
    pricer: Pricer = field(default_factory=Pricer)
    files: int = 0
    warnings: list[str] = field(default_factory=list)

    @property
    def tool_labels(self) -> dict[str, str]:
        return {sid: source.label for sid, source in registry().items()}

    def unknown_models(self) -> list[UnknownModel]:
        return sorted(
            (
                UnknownModel(
                    model=model,
                    tokens=tokens.total,
                    events=self.pricer.unknown_events.get(model, 0),
                )
                for model, tokens in self.pricer.unknown_models.items()
            ),
            key=lambda u: u.tokens,
            reverse=True,
        )


def analyze(
    tools: Sequence[str] | None = None,
    roots: dict[str, list[Path]] | None = None,
    rates_path: Path | None = None,
) -> Analysis:
    scan = scan_all(only=tools, roots=roots)
    pricer = Pricer(RateTable.load(rates_path))
    analysis = Analysis(pricer=pricer, files=scan.files, warnings=list(scan.warnings))
    for event in scan.events:
        cost = pricer.price(event)
        if cost is None:
            continue
        analysis.priced.append(PricedEvent(event=event, cost=cost))
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
    tools: Sequence[str] | None = None,
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
        and (not tools or item.event.tool in tools)
        and (not models or item.event.model in models)
        and (not projects or item.event.project in projects)
        and (include_sidechains or not item.event.is_sidechain)
    ]


def report_of(analysis: Analysis, **filters: object) -> Report:
    priced = filter_events(analysis.priced, **filters)  # type: ignore[arg-type]
    return build_report(
        priced,
        tool_labels=analysis.tool_labels,
        model_label=analysis.pricer.display_name,
        rates_as_of=analysis.pricer.table.as_of,
        files_scanned=analysis.files,
        warnings=analysis.warnings,
        unknown_models=analysis.unknown_models(),
    )


def _as_datetime(day: date | None, at: time) -> datetime | None:
    if day is None:
        return None
    return datetime.combine(day, at).replace(tzinfo=UTC)
