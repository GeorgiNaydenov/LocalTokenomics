from __future__ import annotations

from collections.abc import Iterable, Sequence
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .models import CostBreakdown, CostState, Provenance, RawScalar, TokenUsage, UsageEvent
from .pricing import RateTable, price_event

SpanKind = Literal[
    "turn", "user", "assistant", "reasoning", "model_call", "tool_call",
    "tool_result", "retrieval", "compaction", "error", "subagent",
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

_COST_RANK: dict[CostState, int] = {"priced": 0, "free": 1, "unpriced": 2, "unavailable": 3}
_PROVENANCE_RANK: dict[Provenance, int] = {
    "measured": 0, "derived": 1, "estimated": 2, "inferred": 3, "unavailable": 4,
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
    label: str = ""
    model_calls: int = 0
    tool_calls: int = 0
    tokens: TokenUsage = Field(default_factory=TokenUsage)
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
    if span.tokens is None:
        return None, "unavailable"
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
    total = 0
    found: list[Provenance] = []
    for span in spans:
        if span.duration_ms is None:
            continue
        total += span.duration_ms
        found.append(span.duration_provenance)
    if not found:
        return None, "unavailable"
    return total, max(found, key=lambda p: _PROVENANCE_RANK[p])


def _retries(spans: Sequence[Span]) -> int | None:
    candidates = [span for span in spans if span.kind in ("model_call", "error")]
    if not any(span.retry_attempt is not None for span in candidates):
        return None
    return sum(span.retry_attempt or 0 for span in candidates)


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
    label: str,
    group: Sequence[Span],
    duration_spans: Sequence[Span],
    table: RateTable,
) -> EconRow:
    row = EconRow(key=key, label=label)
    states: list[CostState] = []
    for span in group:
        if span.kind == "model_call":
            row.model_calls += 1
            cost, state = _price_span(span, table)
            states.append(state)
            if cost is not None:
                row.cost = (row.cost or CostBreakdown()) + cost
            if span.tokens is not None:
                row.tokens = row.tokens + span.tokens
        if span.kind in TOOL_KINDS:
            row.tool_calls += 1
        if span.kind == "error" or span.status == "error":
            row.errors += 1
    row.cost_state = max(states, key=lambda s: _COST_RANK[s]) if states else "unavailable"
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
    for span in spans:
        if span.kind == "turn":
            turns[span.turn_id or span.span_id] = span
        if span.turn_id:
            by_turn.setdefault(span.turn_id, []).append(span)
        if span.kind == "model_call":
            by_model.setdefault(span.model or "unknown", []).append(span)
        if span.kind in TOOL_KINDS:
            by_tool.setdefault(span.name or span.kind, []).append(span)

    turn_rows: list[EconRow] = []
    for key, group in by_turn.items():
        turn = turns.get(key)
        label = turn.name if turn is not None and turn.name else key
        turn_rows.append(_econ_row(key, label, group, [turn] if turn is not None else [], table))

    return Economics(
        totals=_econ_row("session", "session", spans, list(turns.values()), table),
        by_turn=turn_rows,
        by_model=sorted(
            (_econ_row(key, key, group, group, table) for key, group in by_model.items()),
            key=lambda r: r.tokens.total,
            reverse=True,
        ),
        by_tool=sorted(
            (_econ_row(key, key, group, group, table) for key, group in by_tool.items()),
            key=lambda r: r.tool_calls,
            reverse=True,
        ),
    )


def context_of(spans: Sequence[Span], table: RateTable) -> list[ContextSnapshot]:
    snapshots: list[ContextSnapshot] = []
    pending: dict[tuple[str, str | None], list[Span]] = {}
    previous: dict[tuple[str, str | None], int] = {}
    for span in spans:
        key = (span.session_id, span.agent_id)
        if span.kind in CONTRIBUTOR_KINDS:
            pending.setdefault(key, []).append(span)
            continue
        if span.kind != "model_call" or span.tokens is None:
            continue
        window = [item for item in pending.pop(key, []) if item.turn_id == span.turn_id]
        capacity = span.context_capacity
        capacity_provenance = span.capacity_provenance
        if capacity_provenance == "unavailable":
            rate = table.lookup(span.model)
            if rate is not None and rate.context_window:
                capacity = rate.context_window
                capacity_provenance = "estimated"
        value, value_provenance = occupancy(
            span.tokens.input_total, capacity, span.tokens_provenance, capacity_provenance
        )
        seen = previous.get(key)
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
                compacted_before=any(item.kind == "compaction" for item in window),
            )
        )
        previous[key] = span.tokens.input_total
    return snapshots


def insights_of(spans: Sequence[Span], economics: Economics) -> list[Insight]:
    found: list[Insight] = []
    anchors = {span.turn_id or span.span_id: span.span_id for span in spans if span.kind == "turn"}

    for row in economics.by_turn:
        anchor = anchors.get(row.key, row.key)
        if row.amplification is not None and row.amplification > AMPLIFICATION_LIMIT:
            found.append(
                Insight(
                    kind="amplification", severity="warning", span_id=anchor,
                    message=(
                        f"this turn read {row.amplification:,.0f} input tokens per output token"
                    ),
                )
            )
        if row.errors >= TURN_ERROR_LIMIT:
            found.append(
                Insight(
                    kind="turn_errors", severity="warning", span_id=anchor,
                    message=f"{row.errors} failed spans in one turn",
                )
            )

    repeats: dict[tuple[str, int], list[str]] = {}
    for span in spans:
        if span.kind in TOOL_KINDS:
            key = (span.name or span.kind, span.record_length)
            repeats.setdefault(key, []).append(span.span_id)
    for (name, _), ids in repeats.items():
        if len(ids) >= REPEATED_TOOL_LIMIT:
            found.append(
                Insight(
                    kind="repeated_tool", severity="info", span_id=ids[0],
                    message=f"{name} ran {len(ids)} times with identically sized arguments",
                )
            )

    for span in spans:
        if span.kind == "tool_result" and span.record_length > LARGE_RESULT_BYTES:
            found.append(
                Insight(
                    kind="large_tool_result", severity="info", span_id=span.span_id,
                    message=f"this tool result records {span.record_length // 1024} KiB",
                )
            )

    calls = [span for span in spans if span.kind == "model_call" and span.tokens is not None]
    for span in calls:
        if span.tokens is None:
            continue
        value, _ = occupancy(
            span.tokens.input_total, span.context_capacity,
            span.tokens_provenance, span.capacity_provenance,
        )
        if value is not None and value > HIGH_OCCUPANCY:
            found.append(
                Insight(
                    kind="context_pressure", severity="warning", span_id=span.span_id,
                    message=f"the context window was {value:.0%} full",
                )
            )

    for span in calls[1:]:
        ratio = cache_hit_ratio(span.tokens)
        if ratio is not None and ratio < LOW_CACHE_HIT_RATIO:
            found.append(
                Insight(
                    kind="cache_miss", severity="info", span_id=span.span_id,
                    message=f"only {ratio:.0%} of this call's input came from the cache",
                )
            )

    first_model = calls[0].model if calls else None
    for span in calls:
        if first_model and span.model and span.model != first_model:
            found.append(
                Insight(
                    kind="model_switch", severity="info", span_id=span.span_id,
                    message=f"the model changed from {first_model} to {span.model} in this session",
                )
            )
            break

    session_tokens = sum(span.tokens.total for span in calls if span.tokens is not None)
    per_agent: dict[str, int] = {}
    for span in calls:
        if span.agent_id and span.tokens is not None:
            per_agent[span.agent_id] = per_agent.get(span.agent_id, 0) + span.tokens.total
    for span in spans:
        if span.kind != "subagent" or not span.agent_id or not session_tokens:
            continue
        share = per_agent.get(span.agent_id, 0) / session_tokens
        if share > SUBAGENT_TOKEN_SHARE:
            found.append(
                Insight(
                    kind="subagent_share", severity="info", span_id=span.span_id,
                    message=f"this subagent used {share:.0%} of the session's tokens",
                )
            )

    for index, span in enumerate(spans):
        if span.kind != "error":
            continue
        for prior in reversed(spans[:index]):
            if prior.kind != "model_call" or prior.tokens is None:
                continue
            if prior.tokens.total > LARGE_CALL_TOKENS:
                found.append(
                    Insight(
                        kind="error_after_large_call", severity="warning", span_id=span.span_id,
                        message=(
                            f"this error followed a {prior.tokens.total:,}-token model call"
                        ),
                    )
                )
            break

    return found
