from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping, Sequence
from datetime import date, datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field

from .models import Bucket, CostBreakdown, CostState, PricedEvent, TokenUsage, local_day
from .sources.base import title_of
from .trace import OutcomeLabel

UNATTRIBUTED = "(no project)"

SessionFlags = Mapping[tuple[str, str], tuple[bool, int, str]]

_STATE_RANK: dict[CostState, int] = {"priced": 0, "free": 1, "unpriced": 2, "unavailable": 3}
# Lower rank wins when picking a session's display title from its events: a tool's own
# title always beats a derived one, and "folder" (no title found at all) is the last resort.
_TITLE_SOURCE_RANK: dict[str, int] = {"tool": 0, "summary": 1, "prompt": 2, "folder": 3}


class Totals(BaseModel):
    tokens: TokenUsage = Field(default_factory=TokenUsage)
    cost: CostBreakdown = Field(default_factory=CostBreakdown)
    events: int = 0
    priced_events: int = 0
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
    has_sidechain: bool = False
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
    title: str | None = None


class UnknownModel(BaseModel):
    model: str
    tokens: int
    events: int


class WarningSeverity(StrEnum):
    """How much a warning's underlying discrepancy affects the numbers shown."""

    # Lowercase members are the serialized API values, not a naming-style slip.
    # pylint: disable=invalid-name
    info = "info"  # cosmetic, no effect on totals
    caution = "caution"  # totals partly affected; the tool bounded or partly corrected it
    critical = "critical"  # totals materially wrong, no correction applied


_SEVERITY_RANK: dict[WarningSeverity, int] = {
    WarningSeverity.info: 0,
    WarningSeverity.caution: 1,
    WarningSeverity.critical: 2,
}


class WarningInstance(BaseModel):
    kind: str
    message: str
    source: str = "unknown"
    file: str | None = None
    session_id: str | None = None
    severity: WarningSeverity = WarningSeverity.info
    delta_tokens: int | None = None  # signed: positive = totals overstated, negative = understated
    delta_cost: float | None = None  # abs(delta_tokens) priced proportionally against the
    # affected session's own token/cost totals, when both are known; None otherwise
    likely_cause: str | None = None
    auto_corrected: bool = False  # true when the parser already applied a partial correction
    # (e.g. subtracting a forked thread's inherited history) before this warning was raised


class WarningGroup(BaseModel):
    kind: str
    label: str
    count: int
    summary: str
    severity: WarningSeverity = WarningSeverity.info
    total_delta_tokens: int = 0
    total_delta_cost: float = 0.0
    worst_example: WarningInstance | None = None
    affected_sessions: int = 0
    instances: list[WarningInstance] = Field(default_factory=list)
    # Deprecated alias, kept for back-compat: [i.message for i in instances].
    warnings: list[str] = Field(default_factory=list)


_WARNING_PATTERNS: list[tuple[str, str, re.Pattern[str]]] = [
    # Codex kinds, most specific first -- all three share a "codex: {name}: ..." prefix, so
    # order matters only in that a later, looser pattern must not shadow an earlier one.
    (
        "codex_counter_reset",
        "Token counter reset mid-session",
        re.compile(r"^codex: .+: counter reset --"),
    ),
    (
        "codex_forked_thread",
        "Forked thread history excluded",
        re.compile(r"^codex: .+: forked thread -- summed turns .+ still unexplained\)$"),
    ),
    ("codex_drift", "Token count drift", re.compile(r"^codex: .+: summed turns .+ drift\)$")),
    ("unparsable_lines", "Unparsable log lines", re.compile(r"skipped \d+ unparsable lines$")),
    ("db_read_error", "Could not read a database file", re.compile(r"cannot read database:")),
    ("chat_data_parse_error", "Could not parse chat data", re.compile(r"cannot parse ")),
    ("read_error", "Could not read a file", re.compile(r"^\S+: cannot read ")),
    ("unknown_model_rate", "Unknown model rate", re.compile(r"^no rate for model ")),
    (
        "inherited_pricing",
        "Priced from a sibling rate",
        re.compile(r"has no exact rates\.json row of its own"),
    ),
    (
        "inert_retention_config",
        "Retention setting has no effect",
        re.compile(r"^content_retention_days is set but inert"),
    ),
]

_DRIFT_PERCENT = re.compile(r"\(([\d.]+)% drift\)$")
_CODEX_FILE = re.compile(r"^codex: ([^:]+):")
_GENERIC_FILE = re.compile(r"^(\S+): ")
_DRIFT_NUMBERS = re.compile(r"summed turns ([\d,]+) vs session total ([\d,]+) \(([\d.]+)% drift\)")
_FORKED_NUMBERS = re.compile(
    r"forked thread -- summed turns ([\d,]+) vs ([\d,]+) after excluding [\d,]+ tokens "
    r"inherited from the parent thread \(([\d.]+)% still unexplained\)"
)

# Heuristic threshold, not sourced from the warnings audit report (which only classified
# *causes*, not a severity cutoff): a residual discrepancy bigger than the file's own
# reported baseline (>100%) reads as "materially wrong"; at or under that, "partly affected".
_CRITICAL_DRIFT_PCT = 100.0

_KIND_SOURCE: dict[str, str] = {
    "codex_drift": "codex",
    "codex_forked_thread": "codex",
    "codex_counter_reset": "codex",
    "unknown_model_rate": "pipeline",
    "inherited_pricing": "pipeline",
    "inert_retention_config": "pipeline",
}

# Kinds whose message text starts with a bare filename ({path.name}: ...) that can be
# resolved to a session via `session_lookup` without the "codex: " wrapper.
_GENERIC_FILE_KINDS = {"unparsable_lines", "chat_data_parse_error"}
_CODEX_KINDS = {"codex_drift", "codex_forked_thread", "codex_counter_reset"}


def _drift_percent(warning: str) -> float:
    match = _DRIFT_PERCENT.search(warning)
    return float(match.group(1)) if match else 0.0


def _int_commas(text: str) -> int:
    return int(text.replace(",", ""))


def _summarize(
    kind: str, label: str, messages: list[str], total_delta_tokens: int, total_delta_cost: float
) -> str:
    if kind == "codex_drift":
        worst = max(messages, key=_drift_percent)
        summary = (
            f"{len(messages)} Codex files disagree with their own reported total, "
            f"the worst by {_drift_percent(worst):.1f}%."
        )
        if total_delta_tokens:
            summary += f" ~{total_delta_tokens:,} tokens affected in total"
            summary += f" (~${total_delta_cost:,.2f})." if total_delta_cost else "."
        return summary
    if kind == "codex_forked_thread":
        summary = (
            f"{len(messages)} forked/resumed Codex thread"
            f"{'s' if len(messages) != 1 else ''} still disagree with their parent-excluded "
            "baseline"
        )
        return (
            f"{summary} (~{total_delta_tokens:,} tokens unexplained)."
            if total_delta_tokens
            else f"{summary}."
        )
    if kind == "codex_counter_reset":
        return (
            f"{len(messages)} Codex session{'s' if len(messages) != 1 else ''} reset "
            "their cumulative token counter mid-file; the final total cannot be used as a "
            "reconciliation baseline."
        )
    if total_delta_tokens:
        return f"{len(messages)} {label.lower()} (~{total_delta_tokens:,} tokens affected)."
    return f"{len(messages)} {label.lower()}."


def _source_of(kind: str, message: str) -> str:
    mapped = _KIND_SOURCE.get(kind)
    if mapped:
        return mapped
    if kind == "read_error":
        match = _GENERIC_FILE.match(message)
        if match:
            return match.group(1)
    return "unknown"


def _file_of(kind: str, message: str) -> str | None:
    if kind in _CODEX_KINDS:
        match = _CODEX_FILE.search(message)
        return match.group(1) if match else None
    if kind in _GENERIC_FILE_KINDS:
        match = _GENERIC_FILE.match(message)
        return match.group(1) if match else None
    return None


# (severity, likely_cause) for kinds that never carry a parseable token delta.
_SIMPLE_CLASSIFICATION: dict[str, tuple[WarningSeverity, str | None]] = {
    "unknown_model_rate": (WarningSeverity.caution, "model missing from rates.json"),
    "inherited_pricing": (
        WarningSeverity.info,
        "priced via a sibling rate row, not an exact match",
    ),
    "inert_retention_config": (
        WarningSeverity.info,
        "config option not implemented in this version",
    ),
    "unparsable_lines": (WarningSeverity.caution, None),
    "db_read_error": (WarningSeverity.caution, None),
    "chat_data_parse_error": (WarningSeverity.caution, None),
    "read_error": (WarningSeverity.caution, None),
}


def _classify_drift_like(
    message: str,
    matcher: re.Pattern[str],
    matched_cause: str,
    unmatched_cause: str | None,
) -> tuple[WarningSeverity, int | None, str | None]:
    """Shared magnitude parsing for `codex_drift` and `codex_forked_thread`: both message
    templates carry `summed turns {n} vs {n} (... {pct}% ...)` in that order."""
    match = matcher.search(message)
    if match is None:
        return WarningSeverity.caution, None, unmatched_cause
    summed, baseline, pct = match.group(1), match.group(2), match.group(3)
    delta = _int_commas(summed) - _int_commas(baseline)
    severity = (
        WarningSeverity.critical if float(pct) > _CRITICAL_DRIFT_PCT else WarningSeverity.caution
    )
    return severity, delta, matched_cause


def _classify(kind: str, message: str) -> tuple[WarningSeverity, int | None, str | None]:
    """Severity, signed token delta, and likely cause for one raw warning string.

    Magnitude is parsed from the message text itself (the existing per-kind templates
    already carry the numbers) rather than requiring every source to change what it
    appends; a message that doesn't match its kind's expected shape just comes back
    unclassified (``None`` delta, ``caution`` severity) instead of raising.
    """
    if kind == "codex_counter_reset":
        return WarningSeverity.critical, None, "mid-session counter reset -- no valid baseline"
    if kind == "codex_forked_thread":
        return _classify_drift_like(
            message,
            _FORKED_NUMBERS,
            "forked/resumed session (parent history excluded)",
            "forked/resumed session",
        )
    if kind == "codex_drift":
        return _classify_drift_like(
            message, _DRIFT_NUMBERS, "duplicate token_count heartbeat emissions", None
        )
    severity, cause = _SIMPLE_CLASSIFICATION.get(kind, (WarningSeverity.info, None))
    return severity, None, cause


def _instance_of(
    warning: str,
    kind: str,
    session_lookup: Mapping[str, str] | None,
    session_totals: Mapping[str, tuple[int, float]] | None,
) -> WarningInstance:
    file = _file_of(kind, warning)
    session_id = session_lookup.get(file) if session_lookup and file else None
    severity, delta_tokens, likely_cause = _classify(kind, warning)
    delta_cost = None
    if delta_tokens is not None and session_id and session_totals:
        totals = session_totals.get(session_id)
        if totals is not None and totals[0] > 0:
            delta_cost = abs(delta_tokens) / totals[0] * totals[1]
    return WarningInstance(
        kind=kind,
        message=warning,
        source=_source_of(kind, warning),
        file=file,
        session_id=session_id,
        severity=severity,
        delta_tokens=delta_tokens,
        delta_cost=delta_cost,
        likely_cause=likely_cause,
        auto_corrected=kind == "codex_forked_thread",
    )


def warning_groups_of(
    warnings: Sequence[str],
    *,
    session_lookup: Mapping[str, str] | None = None,
    session_totals: Mapping[str, tuple[int, float]] | None = None,
) -> list[WarningGroup]:
    """Classify and group raw warning strings, richest-first.

    `session_lookup` maps a warning's file basename (as embedded in its own message text)
    to a session id -- built by the caller from already-available file-to-session data
    (e.g. `SessionRow.raw_source`, or the underlying priced events). `session_totals` maps
    a session id to `(total_tokens, total_cost)`, used only to turn a known `delta_tokens`
    into an estimated `delta_cost` proportional to that session's own totals. Both are
    optional; omitting them still classifies and groups every warning, just without
    `session_id`/`delta_cost` populated on the resulting instances.
    """
    grouped: dict[str, tuple[str, list[WarningInstance]]] = {}
    for warning in warnings:
        kind, label = "other", "Other"
        for candidate_kind, candidate_label, pattern in _WARNING_PATTERNS:
            if pattern.search(warning):
                kind, label = candidate_kind, candidate_label
                break
        instance = _instance_of(warning, kind, session_lookup, session_totals)
        entry = grouped.setdefault(kind, (label, []))
        entry[1].append(instance)

    groups = []
    for kind, (label, instances) in grouped.items():
        messages = [instance.message for instance in instances]
        total_delta_tokens = sum(
            abs(instance.delta_tokens)
            for instance in instances
            if instance.delta_tokens is not None
        )
        total_delta_cost = sum(
            abs(instance.delta_cost) for instance in instances if instance.delta_cost is not None
        )
        worst = max(
            instances,
            key=lambda instance: (
                _SEVERITY_RANK[instance.severity],
                abs(instance.delta_tokens or 0),
            ),
        )
        severity = max(
            (instance.severity for instance in instances), key=lambda item: _SEVERITY_RANK[item]
        )
        affected_sessions = len(
            {instance.session_id for instance in instances if instance.session_id}
        )
        groups.append(
            WarningGroup(
                kind=kind,
                label=label,
                count=len(instances),
                summary=_summarize(kind, label, messages, total_delta_tokens, total_delta_cost),
                severity=severity,
                total_delta_tokens=total_delta_tokens,
                total_delta_cost=total_delta_cost,
                worst_example=worst,
                affected_sessions=affected_sessions,
                instances=instances,
                warnings=messages,
            )
        )
    return sorted(groups, key=lambda g: (g.total_delta_tokens, g.count), reverse=True)


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
    files_in_slice: int = 0
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
            totals.priced_events += 1
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
            event.timestamp.date(),
            event.client,
            event.provider or "unknown",
            event.model or "unknown",
            event.source,
        )
        point = acc.get(key)
        if point is None:
            point = acc[key] = SeriesPoint(
                day=key[0],
                client=key[1],
                provider=key[2],
                model=key[3],
                source=key[4],
                cost=0.0,
                tokens=0,
                events=0,
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
    all_sidechain: dict[tuple[str, str], bool] = {}
    title_rank: dict[tuple[str, str], int] = {}
    title_stamp: dict[tuple[str, str], datetime] = {}
    for item in priced:
        event = item.event
        key = (event.source, event.session_id)
        row = rows.get(key)
        if row is None:
            row = rows[key] = SessionRow(
                session_id=event.session_id,
                source=event.source,
                client=event.client,
                provider=event.provider or "unknown",
                start_time=event.timestamp,
                end_time=event.timestamp,
                currency=currency,
                project=event.project,
                working_directory=event.working_directory,
                repository=event.repository,
                branch=event.branch,
                machine=event.machine,
            )
            models[key] = set()
            states[key] = set()
            sources[key] = set()
            all_sidechain[key] = True
        models[key].add(event.model or "unknown")
        states[key].add(item.state)
        sources[key].add(event.source_file)
        row.start_time = min(row.start_time, event.timestamp)
        row.end_time = max(row.end_time, event.timestamp)
        row.request_count += 1
        row.has_sidechain = row.has_sidechain or event.is_sidechain
        all_sidechain[key] = all_sidechain[key] and event.is_sidechain
        if event.tokens is not None:
            row.tokens = (row.tokens or TokenUsage()) + event.tokens
        if item.cost is not None:
            row.cost = (row.cost or CostBreakdown()) + item.cost
        if row.project is None and event.project:
            row.project = event.project
        # Title needs "prefer highest-ranked title_source seen, then latest" rather than
        # project's first-non-empty-wins: a later 'tool' title must beat an earlier 'folder'
        # fallback, and among same-ranked titles the most recent (e.g. a Claude Code
        # custom-title rename) should win.
        event_rank = _TITLE_SOURCE_RANK.get(event.title_source, _TITLE_SOURCE_RANK["folder"])
        current_rank = title_rank.get(key)
        current_stamp = title_stamp.get(key)
        if (
            current_rank is None
            or event_rank < current_rank
            or (
                event_rank == current_rank
                and (current_stamp is None or event.timestamp >= current_stamp)
            )
        ):
            title_rank[key] = event_rank
            title_stamp[key] = event.timestamp
            row.title = event.title or title_of(event.project, event.session_id)
    for key, row in rows.items():
        row.models = sorted(models[key])
        # Worst-of, matching trace.EconRow.cost_state: a session with any unpriced or
        # unavailable request is not honestly "priced" even if most of it is.
        row.cost_state = max(states[key], key=lambda s: _STATE_RANK[s])
        row.cost_states = sorted(states[key])
        row.is_sidechain = all_sidechain[key]
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
        files_in_slice=len({item.event.source_file for item in priced}),
        totals=totals_of(priced),
        by_client=group(priced, lambda p: p.event.client, lambda k: client_labels.get(k, k)),
        by_provider=group(priced, lambda p: p.event.provider or "unknown"),
        by_model=group(priced, lambda p: p.event.model or "unknown", model_label),
        by_project=group(priced, lambda p: p.event.project or UNATTRIBUTED),
        by_day=group(priced, lambda p: local_day(p.event.timestamp).isoformat()),
        series=series_of(priced),
        sessions=sessions_of(priced, currency, session_flags),
        unknown_models=list(unknown_models),
        warnings=list(warnings),
        scan_warnings=list(scan_warnings),
        # Route the full warning list (not just scan_warnings) so the two pipeline-level
        # kinds -- unknown model rate, inert retention config -- are classified and grouped
        # too, instead of bypassing this entirely as they did before.
        warning_groups=warning_groups_of(
            warnings,
            session_lookup={
                Path(item.event.source_file).name: item.event.session_id for item in priced
            },
        ),
        facets=facets if facets is not None else Facets(),
    )
