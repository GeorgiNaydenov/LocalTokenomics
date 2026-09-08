from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping, Sequence
from datetime import date, datetime

from pydantic import BaseModel, Field

from .models import Bucket, CostBreakdown, CostState, PricedEvent, TokenUsage
from .trace import OutcomeLabel

UNATTRIBUTED = "(no project)"

SessionFlags = Mapping[tuple[str, str], tuple[bool, int, str]]

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
    source: str
    cost: float
    tokens: int
    events: int = 0


class SessionRow(BaseModel):
    session_id: str
    source: str
    client: str
    provider: str
    models: list[str] = Field(default_factory=list)
    start_time: datetime
    end_time: datetime
    request_count: int = 0
    tokens: TokenUsage | None = None
    cost: CostBreakdown | None = None
    cost_state: CostState = "unavailable"
    cost_states: list[CostState] = Field(default_factory=list)
    is_sidechain: bool = False
    currency: str = "USD"
    project: str | None = None
    working_directory: str | None = None
    repository: str | None = None
    branch: str | None = None
    machine: str = ""
    raw_source: list[str] = Field(default_factory=list)
    outcome: OutcomeLabel = "unrated"
    traced: bool = False
    error_count: int = 0


class UnknownModel(BaseModel):
    model: str
    tokens: int
    events: int


class WarningGroup(BaseModel):
    kind: str
    label: str
    count: int
    summary: str
    warnings: list[str] = Field(default_factory=list)


_WARNING_PATTERNS: list[tuple[str, str, re.Pattern[str]]] = [
    ("codex_drift", "Token count drift", re.compile(r"^codex: .+: summed turns .+ drift\)$")),
    ("unparsable_lines", "Unparsable log lines", re.compile(r"skipped \d+ unparsable lines$")),
    ("db_read_error", "Could not read a database file", re.compile(r"cannot read database:")),
    ("chat_data_parse_error", "Could not parse chat data", re.compile(r"cannot parse ")),
    ("read_error", "Could not read a file", re.compile(r"^\S+: cannot read ")),
]

_DRIFT_PERCENT = re.compile(r"\(([\d.]+)% drift\)$")


def _summarize(kind: str, label: str, warnings: list[str]) -> str:
    if kind == "codex_drift":
        worst = max(warnings, key=lambda w: _drift_percent(w))
        return (
            f"{len(warnings)} Codex files disagree with their own reported total, "
            f"the worst by {_drift_percent(worst):.1f}%."
        )
    return f"{len(warnings)} {label.lower()}."


def _drift_percent(warning: str) -> float:
    match = _DRIFT_PERCENT.search(warning)
    return float(match.group(1)) if match else 0.0


def warning_groups_of(warnings: Sequence[str]) -> list[WarningGroup]:
    grouped: dict[str, tuple[str, list[str]]] = {}
    for warning in warnings:
        kind, label = "other", "Other"
        for candidate_kind, candidate_label, pattern in _WARNING_PATTERNS:
            if pattern.search(warning):
                kind, label = candidate_kind, candidate_label
                break
        entry = grouped.setdefault(kind, (label, []))
        entry[1].append(warning)
    groups = [
        WarningGroup(
            kind=kind, label=label, count=len(members),
            summary=_summarize(kind, label, members), warnings=members,
        )
        for kind, (label, members) in grouped.items()
    ]
    return sorted(groups, key=lambda g: g.count, reverse=True)


class Facets(BaseModel):
    states: dict[str, int] = Field(default_factory=dict)
    clients: dict[str, int] = Field(default_factory=dict)
    models: dict[str, int] = Field(default_factory=dict)
    projects: dict[str, int] = Field(default_factory=dict)
    outcomes: dict[str, int] = Field(default_factory=dict)


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
    scan_warnings: list[str] = Field(default_factory=list)
    warning_groups: list[WarningGroup] = Field(default_factory=list)
    facets: Facets = Field(default_factory=Facets)


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
    acc: dict[tuple[date, str, str, str, str], SeriesPoint] = {}
    for item in priced:
        event = item.event
        key = (
            event.timestamp.date(), event.client,
            event.provider or "unknown", event.model or "unknown", event.source,
        )
        point = acc.get(key)
        if point is None:
            point = acc[key] = SeriesPoint(
                day=key[0], client=key[1], provider=key[2], model=key[3], source=key[4],
                cost=0.0, tokens=0, events=0,
            )
        if item.cost is not None:
            point.cost += item.cost.total
        if event.tokens is not None:
            point.tokens += event.tokens.total
        point.events += 1
    return sorted(acc.values(), key=lambda p: (p.day, p.client, p.provider, p.model, p.source))


def sessions_of(
    priced: Iterable[PricedEvent], currency: str, flags: SessionFlags | None = None
) -> list[SessionRow]:
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
        row.is_sidechain = row.is_sidechain or event.is_sidechain
        if event.tokens is not None:
            row.tokens = (row.tokens or TokenUsage()) + event.tokens
        if item.cost is not None:
            row.cost = (row.cost or CostBreakdown()) + item.cost
        if row.project is None and event.project:
            row.project = event.project
    for key, row in rows.items():
        row.models = sorted(models[key])
        row.cost_state = min(states[key], key=lambda s: _STATE_RANK[s])
        row.cost_states = sorted(states[key])
        row.raw_source = sorted(sources[key])
        traced, error_count, outcome = (flags or {}).get(key, (False, 0, "unrated"))
        row.traced = traced
        row.error_count = error_count
        row.outcome = outcome  # type: ignore[assignment]
    return sorted(rows.values(), key=lambda r: r.cost.total if r.cost else 0.0, reverse=True)


def facets_of(priced: Iterable[PricedEvent], flags: SessionFlags | None = None) -> Facets:
    states: dict[str, set[tuple[str, str]]] = {}
    clients: dict[str, set[tuple[str, str]]] = {}
    models: dict[str, set[tuple[str, str]]] = {}
    projects: dict[str, set[tuple[str, str]]] = {}
    outcomes: dict[str, set[tuple[str, str]]] = {}
    for item in priced:
        event = item.event
        session = (event.source, event.session_id)
        states.setdefault(item.state, set()).add(session)
        clients.setdefault(event.client, set()).add(session)
        models.setdefault(event.model or "unknown", set()).add(session)
        projects.setdefault(event.project or UNATTRIBUTED, set()).add(session)
        label = (flags or {}).get(session, (False, 0, "unrated"))[2]
        outcomes.setdefault(label, set()).add(session)
    return Facets(
        states={key: len(sessions) for key, sessions in states.items()},
        clients={key: len(sessions) for key, sessions in clients.items()},
        models={key: len(sessions) for key, sessions in models.items()},
        projects={key: len(sessions) for key, sessions in projects.items()},
        outcomes={key: len(sessions) for key, sessions in outcomes.items()},
    )


def build_report(
    priced: Sequence[PricedEvent],
    *,
    client_labels: dict[str, str],
    model_label: Callable[[str | None], str],
    rates_as_of: str = "",
    currency: str = "USD",
    files_scanned: int = 0,
    warnings: Sequence[str] = (),
    scan_warnings: Sequence[str] = (),
    unknown_models: Sequence[UnknownModel] = (),
    facets: Facets | None = None,
    session_flags: SessionFlags | None = None,
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
        sessions=sessions_of(priced, currency, session_flags),
        unknown_models=list(unknown_models),
        warnings=list(warnings),
        scan_warnings=list(scan_warnings),
        warning_groups=warning_groups_of(scan_warnings),
        facets=facets if facets is not None else Facets(),
    )
