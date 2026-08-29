"""Group priced events into the shapes the terminal table, API and dashboard consume."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from datetime import date, datetime

from pydantic import BaseModel, Field

from .models import Bucket, CostBreakdown, PricedEvent, TokenUsage

UNATTRIBUTED = "(no project)"
"""Bucket for events whose source log carries no working directory, so that
``by_project`` still sums to the grand total instead of quietly dropping them."""


class Totals(BaseModel):
    tokens: TokenUsage = Field(default_factory=TokenUsage)
    cost: CostBreakdown = Field(default_factory=CostBreakdown)
    events: int = 0
    sessions: int = 0
    first_event: datetime | None = None
    last_event: datetime | None = None


class SeriesPoint(BaseModel):
    day: date
    tool: str
    model: str
    cost: float
    tokens: int


class SessionRow(BaseModel):
    session_id: str
    tool: str
    project: str | None = None
    models: list[str] = Field(default_factory=list)
    started: datetime
    ended: datetime
    events: int = 0
    tokens: int = 0
    cost: float = 0.0


class UnknownModel(BaseModel):
    model: str
    tokens: int
    events: int


class Report(BaseModel):
    generated_at: datetime
    rates_as_of: str = ""
    files_scanned: int = 0
    totals: Totals = Field(default_factory=Totals)
    by_tool: list[Bucket] = Field(default_factory=list)
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
        totals.tokens = totals.tokens + item.event.tokens
        totals.cost = totals.cost + item.cost
        totals.events += 1
        sessions.add((item.event.tool, item.event.session_id))
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
        bucket.tokens = bucket.tokens + item.event.tokens
        bucket.cost = bucket.cost + item.cost
        bucket.events += 1
        seen_sessions[raw].add((item.event.tool, item.event.session_id))
    for raw, bucket in buckets.items():
        bucket.sessions = len(seen_sessions[raw])
    return sorted(buckets.values(), key=lambda b: b.cost.total, reverse=True)


def series_of(priced: Iterable[PricedEvent]) -> list[SeriesPoint]:
    """One point per (day, tool, model) -- the dashboard pivots this itself."""
    acc: dict[tuple[date, str, str], SeriesPoint] = {}
    for item in priced:
        key = (item.event.timestamp.date(), item.event.tool, item.event.model)
        point = acc.get(key)
        if point is None:
            point = acc[key] = SeriesPoint(
                day=key[0], tool=key[1], model=key[2], cost=0.0, tokens=0
            )
        point.cost += item.cost.total
        point.tokens += item.event.tokens.total
    return sorted(acc.values(), key=lambda p: (p.day, p.tool, p.model))


def sessions_of(priced: Iterable[PricedEvent]) -> list[SessionRow]:
    rows: dict[tuple[str, str], SessionRow] = {}
    models: dict[tuple[str, str], set[str]] = {}
    for item in priced:
        event = item.event
        key = (event.tool, event.session_id)
        row = rows.get(key)
        if row is None:
            row = rows[key] = SessionRow(
                session_id=event.session_id,
                tool=event.tool,
                project=event.project,
                started=event.timestamp,
                ended=event.timestamp,
            )
            models[key] = set()
        models[key].add(event.model)
        row.started = min(row.started, event.timestamp)
        row.ended = max(row.ended, event.timestamp)
        row.events += 1
        row.tokens += event.tokens.total
        row.cost += item.cost.total
        if row.project is None and event.project:
            row.project = event.project
    for key, row in rows.items():
        row.models = sorted(models[key])
    return sorted(rows.values(), key=lambda r: r.cost, reverse=True)


def build_report(
    priced: Sequence[PricedEvent],
    *,
    tool_labels: dict[str, str],
    model_label: Callable[[str], str],
    rates_as_of: str = "",
    files_scanned: int = 0,
    warnings: Sequence[str] = (),
    unknown_models: Sequence[UnknownModel] = (),
) -> Report:
    return Report(
        generated_at=datetime.now().astimezone(),
        rates_as_of=rates_as_of,
        files_scanned=files_scanned,
        totals=totals_of(priced),
        by_tool=group(priced, lambda p: p.event.tool, lambda k: tool_labels.get(k, k)),
        by_model=group(priced, lambda p: p.event.model, model_label),
        by_project=group(priced, lambda p: p.event.project or UNATTRIBUTED),
        by_day=group(priced, lambda p: p.event.timestamp.date().isoformat()),
        series=series_of(priced),
        sessions=sessions_of(priced),
        unknown_models=list(unknown_models),
        warnings=list(warnings),
    )
