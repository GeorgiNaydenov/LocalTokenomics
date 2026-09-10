from __future__ import annotations

from collections.abc import Iterable, Sequence
from datetime import datetime, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .models import CostBreakdown, CostState, Provenance, RawScalar, TokenUsage, UsageEvent
from .pricing import RateTable, price_event

SpanKind = Literal[
    "turn",
    "user",
    "assistant",
    "reasoning",
    "model_call",
    "tool_call",
    "tool_result",
    "retrieval",
    "compaction",
    "error",
    "subagent",
]
SpanStatus = Literal["ok", "error", "interrupted", "aborted", "running", "unknown"]
OutcomeLabel = Literal["successful", "partial", "failed", "abandoned", "unrated"]

TOOL_KINDS: tuple[SpanKind, ...] = ("tool_call", "retrieval", "subagent")
CONTRIBUTOR_KINDS: tuple[SpanKind, ...] = ("user", "assistant", "tool_result", "compaction")

AMPLIFICATION_LIMIT = 20.0
REPEATED_TOOL_LIMIT = 3
TURN_ERROR_LIMIT = 3
LARGE_RESULT_BYTES = 65_536
HIGH_OCCUPANCY = 0.85
LOW_CACHE_HIT_RATIO = 0.2
SUBAGENT_TOKEN_SHARE = 0.4
LARGE_CALL_TOKENS = 10_000

# Key of the synthetic EconRow that carries spans with no turn_id, so the per-turn
# table can add up to the totals cards above it. Not a real turn_id.
UNATTRIBUTED_TURN_KEY = "unattributed"
UNATTRIBUTED_TURN_LABEL = "Outside any turn"

_COST_RANK: dict[CostState, int] = {"priced": 0, "free": 1, "unpriced": 2, "unavailable": 3}
_PROVENANCE_RANK: dict[Provenance, int] = {
    "measured": 0,
    "derived": 1,
    "estimated": 2,
    "inferred": 3,
    "unavailable": 4,
}


class Span(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    span_id: str
    parent_id: str | None = None
    record_parent: str | None = None
    source: str
    session_id: str
    turn_id: str | None = None
    agent_id: str | None = None
    is_sidechain: bool = False
    seq: int
    kind: SpanKind
    name: str | None = None
    model: str | None = None
    status: SpanStatus = "unknown"
    started_at: datetime
    ended_at: datetime | None = None
    duration_ms: int | None = None
    duration_provenance: Provenance = "unavailable"
    ttft_ms: int | None = None
    tokens: TokenUsage | None = None
    tokens_provenance: Provenance = "unavailable"
    context_capacity: int | None = None
    capacity_provenance: Provenance = "unavailable"
    retry_attempt: int | None = None
    error: str | None = None
    source_file: str
    record_offset: int
    record_length: int
    content_path: str | None = None
    detail: dict[str, RawScalar] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _values_match_provenance(self) -> Span:
        pairs = (
            ("duration_ms", self.duration_ms, self.duration_provenance),
            ("tokens", self.tokens, self.tokens_provenance),
            ("context_capacity", self.context_capacity, self.capacity_provenance),
        )
        for name, value, provenance in pairs:
            if (value is None) != (provenance == "unavailable"):
                raise ValueError(
                    f"{name} is {value!r} but its provenance is {provenance!r}: "
                    "a value is None if and only if its provenance is unavailable"
                )
        return self


class Capabilities(BaseModel):
    trace: Provenance = "unavailable"
    tokens: Provenance = "unavailable"
    cost: Provenance = "unavailable"
    context: Provenance = "unavailable"
    latency: Provenance = "unavailable"


class ContextSnapshot(BaseModel):
    span_id: str
    model: str | None = None
    started_at: datetime
    input_total: int | None = None
    tokens_provenance: Provenance = "unavailable"
    capacity: int | None = None
    capacity_provenance: Provenance = "unavailable"
    occupancy: float | None = None
    occupancy_provenance: Provenance = "unavailable"
    delta_input: int | None = None
    added_span_ids: list[str] = Field(default_factory=list)
    compacted_before: bool = False

    model_config = ConfigDict(protected_namespaces=())


class OutcomeSignals(BaseModel):
    aborted_turns: int = 0
    interrupted_tools: int = 0
    errors: int = 0
    last_turn_status: SpanStatus = "unknown"


class OutcomeUpdate(BaseModel):
    outcome: OutcomeLabel = "unrated"
    notes: str = ""
    tags: list[str] = Field(default_factory=list)


class Outcome(OutcomeUpdate):
    source: str
    session_id: str
    updated_at: datetime | None = None
    signals: OutcomeSignals = Field(default_factory=OutcomeSignals)


class EconRow(BaseModel):
    key: str
    label: str | None = ""
    ordinal: int | None = None
    started_at: datetime | None = None
    is_sidechain: bool = False
    model_calls: int = 0
    tool_calls: int = 0
    tokens: TokenUsage | None = None
    tokens_provenance: Provenance = "unavailable"
    cost: CostBreakdown | None = None
    cost_state: CostState = "unavailable"
    duration_ms: int | None = None
    duration_provenance: Provenance = "unavailable"
    errors: int = 0
    retries: int | None = None
    amplification: float | None = None
    cache_hit_ratio: float | None = None
    tokens_per_second: float | None = None

    model_config = ConfigDict(protected_namespaces=())


class Economics(BaseModel):
    totals: EconRow
    by_turn: list[EconRow] = Field(default_factory=list)
    by_model: list[EconRow] = Field(default_factory=list)
    by_tool: list[EconRow] = Field(default_factory=list)


class Insight(BaseModel):
    kind: str
    severity: Literal["info", "warning", "critical"] = "info"
    span_id: str
    message: str
    count: int = 1


class Trace(BaseModel):
    source: str
    session_id: str
    capabilities: Capabilities = Field(default_factory=Capabilities)
    spans: list[Span] = Field(default_factory=list)
    outcome: Outcome | None = None
    insights: list[Insight] = Field(default_factory=list)


class SpanContent(BaseModel):
    span_id: str
    content: str
    truncated: bool = False
    redactions: int = 0


def amplification(spans: Iterable[Span]) -> float | None:
    input_total = 0
    output = 0
    for span in spans:
        if span.kind == "model_call" and span.tokens is not None:
            input_total += span.tokens.input_total
            output += span.tokens.output
    if output == 0:
        return None
    return input_total / output


def cache_hit_ratio(tokens: TokenUsage | None) -> float | None:
    if tokens is None or tokens.input_total == 0:
        return None
    return tokens.cache_read / tokens.input_total


def tokens_per_second(span: Span) -> float | None:
    if span.tokens is None or span.tokens_provenance != "measured":
        return None
    if span.duration_provenance != "measured" or not span.duration_ms:
        return None
    return span.tokens.output / (span.duration_ms / 1000)


def occupancy(
    input_total: int | None,
    capacity: int | None,
    tokens_provenance: Provenance,
    capacity_provenance: Provenance,
) -> tuple[float | None, Provenance]:
    if input_total is None or not capacity or tokens_provenance == "unavailable":
        return None, "unavailable"
    if tokens_provenance == "measured" and capacity_provenance == "measured":
        return input_total / capacity, "derived"
    if capacity_provenance in ("estimated", "inferred"):
        return input_total / capacity, "estimated"
    return None, "unavailable"


def _price_span(span: Span, table: RateTable) -> tuple[CostBreakdown | None, CostState]:
    tier = span.detail.get("tier")
    event = UsageEvent(
        source=span.source,
        client=span.source,
        model=span.model,
        timestamp=span.started_at,
        session_id=span.session_id,
        tokens=span.tokens,
        tier=tier if isinstance(tier, str) and tier else "standard",
    )
    return price_event(event, table)


def _summed_duration(spans: Sequence[Span]) -> tuple[int | None, Provenance]:
    """Active time covered by these spans: a union of their (started_at, ended_at)
    intervals, not a naive sum. A nested subagent turn that runs entirely inside its
    parent turn therefore adds nothing to the total; two disjoint turns each count in
    full. Provenance is the worst among the spans that contributed an interval.
    """
    intervals: list[tuple[datetime, datetime, Provenance]] = []
    for span in spans:
        if span.duration_ms is None:
            continue
        end = span.started_at + timedelta(milliseconds=span.duration_ms)
        intervals.append((span.started_at, end, span.duration_provenance))
    if not intervals:
        return None, "unavailable"
    intervals.sort(key=lambda item: item[0])
    found: list[Provenance] = [intervals[0][2]]
    total_ms = 0.0
    current_start, current_end, _ = intervals[0]
    for start, end, provenance in intervals[1:]:
        found.append(provenance)
        if start > current_end:
            total_ms += (current_end - current_start).total_seconds() * 1000
            current_start, current_end = start, end
        elif end > current_end:
            current_end = end
    total_ms += (current_end - current_start).total_seconds() * 1000
    return round(total_ms), max(found, key=lambda p: _PROVENANCE_RANK[p])


def _retries(spans: Sequence[Span]) -> int | None:
    """`retry_attempt` is not one thing across producers: Claude Code's `api_error`
    records carry an attempt *index* (1, 2, 3, ... for the same underlying request), while
    its usage-iterations count is already a genuine number of extra attempts. Summing both
    as if they were the same unit overstates retries (three index records 1/2/3 would sum
    to 6 instead of 3). We take the max of the index-shaped values, once, and add that to
    the sum of the count-shaped values.
    """
    error_indices = [
        span.retry_attempt
        for span in spans
        if span.kind == "error" and span.retry_attempt is not None
    ]
    call_counts = [
        span.retry_attempt
        for span in spans
        if span.kind == "model_call" and span.retry_attempt is not None
    ]
    if not error_indices and not call_counts:
        return None
    return (max(error_indices) if error_indices else 0) + sum(call_counts)


def tool_result_parent_ids(spans: Iterable[Span]) -> set[str]:
    """span_ids of tool_call/retrieval/subagent spans that are closed by a `tool_result`
    span. Claude Code and Codex both copy the result's status onto the call span that
    opened it (`_close_call` / the function_call_output handler), so a failing call and
    its failing result carry `status == "error"` twice for the same underlying failure.
    """
    return {span.parent_id for span in spans if span.kind == "tool_result" and span.parent_id}


def is_error_span(span: Span, tool_result_parents: set[str]) -> bool:
    """Whether this span should count as one failure. An `error`-kind span always counts;
    a `tool_result` with `status == "error"` always counts. A tool_call/retrieval/subagent
    span counts only when it has no paired `tool_result` (e.g. Antigravity and Codex's MCP
    path, which set status directly with no separate result span) — when a paired result
    exists, that result already counts the failure, so the call span is skipped to avoid
    counting the same failure twice. Any other span kind with `status == "error"` counts.
    """
    if span.kind == "error":
        return True
    if span.status != "error":
        return False
    if span.kind == "tool_result":
        return True
    if span.kind in TOOL_KINDS:
        return span.span_id not in tool_result_parents
    return True


def _measured_rate(spans: Sequence[Span]) -> float | None:
    output = 0
    duration = 0
    for span in spans:
        if span.tokens is None or span.duration_ms is None:
            continue
        if tokens_per_second(span) is None:
            continue
        output += span.tokens.output
        duration += span.duration_ms
    if duration == 0:
        return None
    return output / (duration / 1000)


def _econ_row(
    key: str,
    label: str | None,
    group: Sequence[Span],
    duration_spans: Sequence[Span],
    table: RateTable,
    tool_result_parents: set[str],
) -> EconRow:
    row = EconRow(key=key, label=label)
    states: list[CostState] = []
    provenances: list[Provenance] = []
    for span in group:
        if span.kind == "model_call":
            row.model_calls += 1
            cost, state = _price_span(span, table)
            states.append(state)
            if cost is not None:
                row.cost = (row.cost or CostBreakdown()) + cost
            if span.tokens is not None:
                row.tokens = (row.tokens or TokenUsage()) + span.tokens
                provenances.append(span.tokens_provenance)
        if span.kind in TOOL_KINDS:
            row.tool_calls += 1
        if is_error_span(span, tool_result_parents):
            row.errors += 1
    row.cost_state = max(states, key=lambda s: _COST_RANK[s]) if states else "unavailable"
    row.tokens_provenance = (
        max(provenances, key=lambda p: _PROVENANCE_RANK[p]) if provenances else "unavailable"
    )
    row.duration_ms, row.duration_provenance = _summed_duration(duration_spans)
    row.retries = _retries(group)
    row.amplification = amplification(group)
    row.cache_hit_ratio = cache_hit_ratio(row.tokens) if row.model_calls else None
    row.tokens_per_second = _measured_rate(group)
    return row


def economics_of(spans: Sequence[Span], table: RateTable) -> Economics:
    turns: dict[str, Span] = {}
    by_turn: dict[str, list[Span]] = {}
    by_model: dict[str, list[Span]] = {}
    by_tool: dict[str, list[Span]] = {}
    turnless: list[Span] = []
    for span in spans:
        if span.kind == "turn":
            turns[span.turn_id or span.span_id] = span
        if span.turn_id:
            by_turn.setdefault(span.turn_id, []).append(span)
        else:
            turnless.append(span)
        if span.kind == "model_call":
            by_model.setdefault(span.model or "unknown", []).append(span)
        if span.kind in TOOL_KINDS:
            by_tool.setdefault(span.name or span.kind, []).append(span)

    tool_result_parents = tool_result_parent_ids(spans)

    turn_rows: list[EconRow] = []
    for ordinal, (key, group) in enumerate(by_turn.items(), start=1):
        turn = turns.get(key)
        row = _econ_row(
            key,
            turn.name if turn is not None else None,
            group,
            [turn] if turn is not None else [],
            table,
            tool_result_parents,
        )
        row.ordinal = ordinal
        row.started_at = turn.started_at if turn is not None else None
        row.is_sidechain = turn.is_sidechain if turn is not None else False
        turn_rows.append(row)

    if turnless:
        turn_rows.append(
            _econ_row(
                UNATTRIBUTED_TURN_KEY,
                UNATTRIBUTED_TURN_LABEL,
                turnless,
                [],
                table,
                tool_result_parents,
            )
        )

    return Economics(
        totals=_econ_row(
            "session", "session", spans, list(turns.values()), table, tool_result_parents
        ),
        by_turn=turn_rows,
        by_model=sorted(
            (
                _econ_row(key, key, group, group, table, tool_result_parents)
                for key, group in by_model.items()
            ),
            key=lambda r: r.tokens.total if r.tokens is not None else 0,
            reverse=True,
        ),
        by_tool=sorted(
            (
                _econ_row(key, key, group, group, table, tool_result_parents)
                for key, group in by_tool.items()
            ),
            key=lambda r: r.tool_calls,
            reverse=True,
        ),
    )


def _capacity_of(span: Span, table: RateTable) -> tuple[int | None, Provenance]:
    """Context capacity for one model call: the span's own measurement if the source
    logged one, else the rate table's `context_window` for that model, marked estimated.
    Shared by `context_of` (the Context tab) and `insights_of` (the `context_pressure`
    insight) so the two never disagree about whether a capacity is known.
    """
    if span.capacity_provenance != "unavailable":
        return span.context_capacity, span.capacity_provenance
    rate = table.lookup(span.model)
    if rate is not None and rate.context_window:
        return rate.context_window, "estimated"
    return None, "unavailable"


def context_of(spans: Sequence[Span], table: RateTable) -> list[ContextSnapshot]:
    snapshots: list[ContextSnapshot] = []
    pending: dict[tuple[str, str | None], list[Span]] = {}
    previous: dict[tuple[str, str | None], int] = {}
    compacted: dict[tuple[str, str | None], bool] = {}
    for span in spans:
        key = (span.session_id, span.agent_id)
        if span.kind in CONTRIBUTOR_KINDS:
            pending.setdefault(key, []).append(span)
            if span.kind == "compaction":
                compacted[key] = True
            continue
        if span.kind != "model_call" or span.tokens is None:
            continue
        # Partition, don't pop: contributors from a turn other than this call's are kept
        # pending rather than discarded, so a later call belonging to that turn still sees
        # them (B20 — a compaction landing at the end of one turn must still be visible to
        # the first model call of the next turn, which is a different turn_id).
        queued = pending.get(key, [])
        window = [item for item in queued if item.turn_id == span.turn_id]
        pending[key] = [item for item in queued if item.turn_id != span.turn_id]
        capacity, capacity_provenance = _capacity_of(span, table)
        value, value_provenance = occupancy(
            span.tokens.input_total, capacity, span.tokens_provenance, capacity_provenance
        )
        seen = previous.get(key)
        # "Compaction seen since the last model call" is tracked as a latch per
        # (session, agent), independent of turn boundaries, because compaction lands at
        # the end of one turn while the next model call belongs to the next turn — the
        # old turn_id-scoped window meant this flag was never true (§4.9).
        compacted_before = compacted.get(key, False)
        compacted[key] = False
        snapshots.append(
            ContextSnapshot(
                span_id=span.span_id,
                model=span.model,
                started_at=span.started_at,
                input_total=span.tokens.input_total,
                tokens_provenance=span.tokens_provenance,
                capacity=capacity,
                capacity_provenance=capacity_provenance,
                occupancy=value,
                occupancy_provenance=value_provenance,
                delta_input=None if seen is None else span.tokens.input_total - seen,
                added_span_ids=[item.span_id for item in window],
                compacted_before=compacted_before,
            )
        )
        previous[key] = span.tokens.input_total
    return snapshots


Occurrence = tuple[str, float]


def _worst(occurrences: list[Occurrence], *, smallest: bool = False) -> Occurrence:
    pick = min if smallest else max
    return pick(occurrences, key=lambda o: o[1])


def _paid_amplification(tokens: TokenUsage | None) -> float | None:
    """Ratio of tokens paid at full rate (uncached input plus cache writes — the tokens
    that were not already sitting in the cache) to output tokens. Unlike the displayed
    `amplification` field (input_total / output, which includes cheap cache reads and is
    routinely 30-500x on any normally cached agent turn), this is the ratio the
    `amplification` insight fires on, so the insight flags turns that are actually
    reading expensive tokens rather than every turn with a warm cache.
    """
    if tokens is None or tokens.output == 0:
        return None
    return (tokens.uncached_input + tokens.cache_write) / tokens.output


def _amplification_insight(occurrences: list[Occurrence]) -> Insight:
    span_id, value = _worst(occurrences)
    if len(occurrences) == 1:
        message = (
            f"This turn read {value:,.0f} full-price (uncached) input tokens for every "
            "output token it produced."
        )
    else:
        message = (
            f"{len(occurrences)} turns each read more than {AMPLIFICATION_LIMIT:.0f} "
            "full-price (uncached) input tokens per output token, the heaviest reading "
            f"{value:,.0f} to one."
        )
    return Insight(
        kind="amplification",
        severity="warning",
        span_id=span_id,
        message=message,
        count=len(occurrences),
    )


def _turn_errors_insight(occurrences: list[Occurrence]) -> Insight:
    span_id, value = _worst(occurrences)
    if len(occurrences) == 1:
        message = f"This turn had {value:.0f} failed spans."
    else:
        message = (
            f"{len(occurrences)} turns each had {TURN_ERROR_LIMIT} or more failed spans, the worst "
            f"turn failing {value:.0f} spans."
        )
    return Insight(
        kind="turn_errors",
        severity="warning",
        span_id=span_id,
        message=message,
        count=len(occurrences),
    )


def _repeated_tool_insight(occurrences: list[Occurrence], names: dict[str, str]) -> Insight:
    span_id, value = _worst(occurrences)
    if len(occurrences) == 1:
        message = f"{names[span_id]} ran {value:.0f} times with identically sized arguments."
    else:
        message = (
            f"{len(occurrences)} different tool calls each repeated {REPEATED_TOOL_LIMIT} or more "
            f"times with identical arguments, the most repeated running {value:.0f} times."
        )
    return Insight(
        kind="repeated_tool",
        severity="info",
        span_id=span_id,
        message=message,
        count=len(occurrences),
    )


def _large_tool_result_insight(occurrences: list[Occurrence]) -> Insight:
    span_id, value = _worst(occurrences)
    if len(occurrences) == 1:
        message = f"This tool result records {value:,.0f} KiB."
    else:
        message = (
            f"{len(occurrences)} tool results were larger than {LARGE_RESULT_BYTES // 1024} KiB, "
            f"the largest at {value:,.0f} KiB."
        )
    return Insight(
        kind="large_tool_result",
        severity="info",
        span_id=span_id,
        message=message,
        count=len(occurrences),
    )


def _context_pressure_insight(occurrences: list[Occurrence]) -> Insight:
    span_id, value = _worst(occurrences)
    if len(occurrences) == 1:
        message = f"The context window was {value:.0%} full on this call."
    else:
        message = (
            f"{len(occurrences)} model calls filled the context window past {HIGH_OCCUPANCY:.0%}, "
            f"peaking at {value:.0%}."
        )
    return Insight(
        kind="context_pressure",
        severity="warning",
        span_id=span_id,
        message=message,
        count=len(occurrences),
    )


def _cache_miss_insight(occurrences: list[Occurrence]) -> Insight:
    span_id, value = _worst(occurrences, smallest=True)
    if len(occurrences) == 1:
        message = f"Only {value:.0%} of this call's input came from the cache."
    else:
        message = (
            f"{len(occurrences)} model calls served less than {LOW_CACHE_HIT_RATIO:.0%} of their "
            f"input from the cache, the lowest at {value:.0%}."
        )
    return Insight(
        kind="cache_miss",
        severity="info",
        span_id=span_id,
        message=message,
        count=len(occurrences),
    )


def _subagent_share_insight(occurrences: list[Occurrence]) -> Insight:
    span_id, value = _worst(occurrences)
    if len(occurrences) == 1:
        message = f"This subagent used {value:.0%} of the session's tokens."
    else:
        message = (
            f"{len(occurrences)} subagents each used more than {SUBAGENT_TOKEN_SHARE:.0%} of the "
            f"session's tokens, the heaviest using {value:.0%}."
        )
    return Insight(
        kind="subagent_share",
        severity="info",
        span_id=span_id,
        message=message,
        count=len(occurrences),
    )


def _error_after_large_call_insight(occurrences: list[Occurrence]) -> Insight:
    span_id, value = _worst(occurrences)
    if len(occurrences) == 1:
        message = f"This error followed a {value:,.0f}-token model call."
    else:
        message = (
            f"{len(occurrences)} errors each followed a model call over {LARGE_CALL_TOKENS:,} "
            f"tokens, the largest call reading {value:,.0f} tokens."
        )
    return Insight(
        kind="error_after_large_call",
        severity="warning",
        span_id=span_id,
        message=message,
        count=len(occurrences),
    )


def insights_of(spans: Sequence[Span], economics: Economics, table: RateTable) -> list[Insight]:
    found: list[Insight] = []
    anchors = {span.turn_id or span.span_id: span.span_id for span in spans if span.kind == "turn"}

    amplification_hits: list[Occurrence] = []
    turn_error_hits: list[Occurrence] = []
    for row in economics.by_turn:
        if row.key == UNATTRIBUTED_TURN_KEY:
            continue  # not a real span_id; spans without a turn_id have nothing to anchor to
        anchor = anchors.get(row.key, row.key)
        paid_ratio = _paid_amplification(row.tokens)
        if paid_ratio is not None and paid_ratio > AMPLIFICATION_LIMIT:
            amplification_hits.append((anchor, paid_ratio))
        if row.errors >= TURN_ERROR_LIMIT:
            turn_error_hits.append((anchor, row.errors))
    if amplification_hits:
        found.append(_amplification_insight(amplification_hits))
    if turn_error_hits:
        found.append(_turn_errors_insight(turn_error_hits))

    repeats: dict[tuple[str, int], list[str]] = {}
    for span in spans:
        if span.kind in TOOL_KINDS:
            key = (span.name or span.kind, span.record_length)
            repeats.setdefault(key, []).append(span.span_id)
    repeated_tool_hits: list[Occurrence] = []
    repeated_tool_names: dict[str, str] = {}
    for (name, _), ids in repeats.items():
        if len(ids) >= REPEATED_TOOL_LIMIT:
            repeated_tool_hits.append((ids[0], len(ids)))
            repeated_tool_names[ids[0]] = name
    if repeated_tool_hits:
        found.append(_repeated_tool_insight(repeated_tool_hits, repeated_tool_names))

    large_result_hits: list[Occurrence] = [
        (span.span_id, span.record_length / 1024)
        for span in spans
        if span.kind == "tool_result" and span.record_length > LARGE_RESULT_BYTES
    ]
    if large_result_hits:
        found.append(_large_tool_result_insight(large_result_hits))

    calls = [span for span in spans if span.kind == "model_call" and span.tokens is not None]
    context_pressure_hits: list[Occurrence] = []
    for span in calls:
        if span.tokens is None:
            continue
        capacity, capacity_provenance = _capacity_of(span, table)
        value, _ = occupancy(
            span.tokens.input_total,
            capacity,
            span.tokens_provenance,
            capacity_provenance,
        )
        if value is not None and value > HIGH_OCCUPANCY:
            context_pressure_hits.append((span.span_id, value))
    if context_pressure_hits:
        found.append(_context_pressure_insight(context_pressure_hits))

    cache_miss_hits: list[Occurrence] = []
    for span in calls[1:]:
        ratio = cache_hit_ratio(span.tokens)
        if ratio is not None and ratio < LOW_CACHE_HIT_RATIO:
            cache_miss_hits.append((span.span_id, ratio))
    if cache_miss_hits:
        found.append(_cache_miss_insight(cache_miss_hits))

    first_model = calls[0].model if calls else None
    for span in calls:
        if first_model and span.model and span.model != first_model:
            found.append(
                Insight(
                    kind="model_switch",
                    severity="info",
                    span_id=span.span_id,
                    message=(
                        f"The model changed from {first_model} to {span.model} in this session."
                    ),
                )
            )
            break

    session_tokens = sum(span.tokens.total for span in calls if span.tokens is not None)
    per_agent: dict[str, int] = {}
    for span in calls:
        if span.agent_id and span.tokens is not None:
            per_agent[span.agent_id] = per_agent.get(span.agent_id, 0) + span.tokens.total
    subagent_share_hits: list[Occurrence] = []
    for span in spans:
        if span.kind != "subagent" or not span.agent_id or not session_tokens:
            continue
        share = per_agent.get(span.agent_id, 0) / session_tokens
        if share > SUBAGENT_TOKEN_SHARE:
            subagent_share_hits.append((span.span_id, share))
    if subagent_share_hits:
        found.append(_subagent_share_insight(subagent_share_hits))

    error_after_large_call_hits: list[Occurrence] = []
    for index, span in enumerate(spans):
        if span.kind != "error":
            continue
        for prior in reversed(spans[:index]):
            if prior.kind != "model_call" or prior.tokens is None:
                continue
            if prior.tokens.total > LARGE_CALL_TOKENS:
                error_after_large_call_hits.append((span.span_id, prior.tokens.total))
            break
    if error_after_large_call_hits:
        found.append(_error_after_large_call_insight(error_after_large_call_hits))

    return found
