from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from datetime import date, datetime

from pydantic import BaseModel, Field

from .models import Bucket, CostBreakdown, CostState, PricedEvent, TokenUsage

UNATTRIBUTED = "(no project)"

_STATE_RANK: dict[CostState, int] = {"priced": 0, "free": 1, "unpriced": 2, "unavailable": 3}


class Totals(BaseModel):
    tokens: TokenUsage = Field(default_factory=TokenUsage)
    cost: CostBreakdown = Field(default_factory=CostBreakdown)
    events: int = 0
    sessions: int = 0
    first_event: datetime | None = None
    last_event: datetime | None = None


class SeriesPoint(BaseModel):
    day: date
    client: str
    provider: str
    model: str
    cost: float
    tokens: int


class SessionRow(BaseModel):
    session_id: str
    source: str
    client: str
    provider: str
    models: list[str] = Field(default_factory=list)
    start_time: datetime
    end_time: datetime
    request_count: int = 0
    input_tokens: int | None = None
    output_tokens: int | None = None
    cached_tokens: int | None = None
    reasoning_tokens: int | None = None
    cost: float | None = None
    cost_state: CostState = "unavailable"
    currency: str = "USD"
    project: str | None = None
    working_directory: str | None = None
    repository: str | None = None
    branch: str | None = None
    machine: str = ""
    raw_source: list[str] = Field(default_factory=list)


class UnknownModel(BaseModel):
    model: str
    tokens: int
    events: int


class Report(BaseModel):
    generated_at: datetime
    rates_as_of: str = ""
    currency: str = "USD"
    files_scanned: int = 0
    totals: Totals = Field(default_factory=Totals)
    by_client: list[Bucket] = Field(default_factory=list)
    by_provider: list[Bucket] = Field(default_factory=list)
    by_model: list[Bucket] = Field(default_factory=list)
    by_project: list[Bucket] = Field(default_factory=list)
    by_day: list[Bucket] = Field(default_factory=list)
    series: list[SeriesPoint] = Field(default_factory=list)
    sessions: list[SessionRow] = Field(default_factory=list)
    unknown_models: list[UnknownModel] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


def totals_of(priced: Sequence[PricedEvent]) -> Totals:
    totals = Totals()
    sessions: set[tuple[str, str]] = set()
    for item in priced:
        if item.event.tokens is not None:
            totals.tokens = totals.tokens + item.event.tokens
        if item.cost is not None:
            totals.cost = totals.cost + item.cost
        totals.events += 1
        sessions.add((item.event.source, item.event.session_id))
        stamp = item.event.timestamp
        if totals.first_event is None or stamp < totals.first_event:
            totals.first_event = stamp
        if totals.last_event is None or stamp > totals.last_event:
            totals.last_event = stamp
    totals.sessions = len(sessions)
    return totals


def group(
    priced: Iterable[PricedEvent],
    key: Callable[[PricedEvent], str | None],
    label: Callable[[str], str] | None = None,
) -> list[Bucket]:
    buckets: dict[str, Bucket] = {}
    seen_sessions: dict[str, set[tuple[str, str]]] = {}
    for item in priced:
        raw = key(item)
        if raw is None:
            continue
        bucket = buckets.get(raw)
        if bucket is None:
            bucket = buckets[raw] = Bucket(key=raw, label=label(raw) if label else raw)
            seen_sessions[raw] = set()
        if item.event.tokens is not None:
            bucket.tokens = bucket.tokens + item.event.tokens
        if item.cost is not None:
            bucket.cost = bucket.cost + item.cost
        bucket.events += 1
        seen_sessions[raw].add((item.event.source, item.event.session_id))
    for raw, bucket in buckets.items():
        bucket.sessions = len(seen_sessions[raw])
    return sorted(buckets.values(), key=lambda b: b.cost.total, reverse=True)


def series_of(priced: Iterable[PricedEvent]) -> list[SeriesPoint]:
    acc: dict[tuple[date, str, str, str], SeriesPoint] = {}
    for item in priced:
        event = item.event
        key = (
            event.timestamp.date(), event.client,
            event.provider or "unknown", event.model or "unknown",
        )
        point = acc.get(key)
        if point is None:
            point = acc[key] = SeriesPoint(
                day=key[0], client=key[1], provider=key[2], model=key[3], cost=0.0, tokens=0
            )
        if item.cost is not None:
            point.cost += item.cost.total
        if event.tokens is not None:
            point.tokens += event.tokens.total
    return sorted(acc.values(), key=lambda p: (p.day, p.client, p.provider, p.model))


def sessions_of(priced: Iterable[PricedEvent], currency: str) -> list[SessionRow]:
    rows: dict[tuple[str, str], SessionRow] = {}
    models: dict[tuple[str, str], set[str]] = {}
    states: dict[tuple[str, str], set[CostState]] = {}
    sources: dict[tuple[str, str], set[str]] = {}
    for item in priced:
        event = item.event
        key = (event.source, event.session_id)
        row = rows.get(key)
        if row is None:
            row = rows[key] = SessionRow(
                session_id=event.session_id, source=event.source, client=event.client,
                provider=event.provider or "unknown", start_time=event.timestamp,
                end_time=event.timestamp, currency=currency, project=event.project,
                working_directory=event.working_directory, repository=event.repository,
                branch=event.branch, machine=event.machine,
            )
            models[key] = set()
            states[key] = set()
            sources[key] = set()
        models[key].add(event.model or "unknown")
        states[key].add(item.state)
        sources[key].add(event.source_file)
        row.start_time = min(row.start_time, event.timestamp)
        row.end_time = max(row.end_time, event.timestamp)
        row.request_count += 1
        if event.tokens is not None:
            row.input_tokens = (row.input_tokens or 0) + event.tokens.input_total
            row.output_tokens = (row.output_tokens or 0) + event.tokens.output
            row.cached_tokens = (row.cached_tokens or 0) + event.tokens.cache_read
            row.reasoning_tokens = (row.reasoning_tokens or 0) + event.tokens.reasoning_output
        if item.cost is not None:
            row.cost = (row.cost or 0.0) + item.cost.total
        if row.project is None and event.project:
            row.project = event.project
    for key, row in rows.items():
        row.models = sorted(models[key])
        row.cost_state = min(states[key], key=lambda s: _STATE_RANK[s])
        row.raw_source = sorted(sources[key])
    return sorted(rows.values(), key=lambda r: r.cost or 0.0, reverse=True)


def build_report(
    priced: Sequence[PricedEvent],
    *,
    client_labels: dict[str, str],
    model_label: Callable[[str | None], str],
    rates_as_of: str = "",
    currency: str = "USD",
    files_scanned: int = 0,
    warnings: Sequence[str] = (),
    unknown_models: Sequence[UnknownModel] = (),
) -> Report:
    return Report(
        generated_at=datetime.now().astimezone(),
        rates_as_of=rates_as_of,
        currency=currency,
        files_scanned=files_scanned,
        totals=totals_of(priced),
        by_client=group(priced, lambda p: p.event.client, lambda k: client_labels.get(k, k)),
        by_provider=group(priced, lambda p: p.event.provider or "unknown"),
        by_model=group(priced, lambda p: p.event.model or "unknown", model_label),
        by_project=group(priced, lambda p: p.event.project or UNATTRIBUTED),
        by_day=group(priced, lambda p: p.event.timestamp.date().isoformat()),
        series=series_of(priced),
        sessions=sessions_of(priced, currency),
        unknown_models=list(unknown_models),
        warnings=list(warnings),
    )
