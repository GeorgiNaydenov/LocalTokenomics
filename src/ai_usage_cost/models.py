"""Core data model.

Everything downstream of parsing works on :class:`UsageEvent`, so no source module
needs to know that any other source exists.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, computed_field


class TokenUsage(BaseModel):
    """Billable token counts for one request, normalised across providers.

    The four billable buckets are disjoint: a token is counted in exactly one of
    ``uncached_input``, ``cache_read``, ``cache_write_5m`` / ``cache_write_1h``, or
    ``output``. ``reasoning_output`` and ``thinking_output`` are *subsets* of
    ``output`` kept for display only -- never add them to a total.
    """

    uncached_input: int = 0
    cache_read: int = 0
    cache_write_5m: int = 0
    cache_write_1h: int = 0
    output: int = 0

    reasoning_output: int = 0
    thinking_output: int = 0

    @computed_field  # type: ignore[prop-decorator]
    @property
    def cache_write(self) -> int:
        return self.cache_write_5m + self.cache_write_1h

    @computed_field  # type: ignore[prop-decorator]
    @property
    def input_total(self) -> int:
        return self.uncached_input + self.cache_read + self.cache_write

    @computed_field  # type: ignore[prop-decorator]
    @property
    def total(self) -> int:
        return self.input_total + self.output

    def __add__(self, other: TokenUsage) -> TokenUsage:
        return TokenUsage(
            uncached_input=self.uncached_input + other.uncached_input,
            cache_read=self.cache_read + other.cache_read,
            cache_write_5m=self.cache_write_5m + other.cache_write_5m,
            cache_write_1h=self.cache_write_1h + other.cache_write_1h,
            output=self.output + other.output,
            reasoning_output=self.reasoning_output + other.reasoning_output,
            thinking_output=self.thinking_output + other.thinking_output,
        )


class UsageEvent(BaseModel):
    """One billable request, parsed out of a local CLI log."""

    tool: str
    """Source id, e.g. ``claude-code`` or ``codex``."""

    timestamp: datetime
    model: str
    session_id: str
    project: str | None = None
    tokens: TokenUsage = Field(default_factory=TokenUsage)

    is_sidechain: bool = False
    """True for subagent / sidechain requests, so their spend can be split out."""

    tier: str = "standard"
    """``standard``, ``batch`` or ``fast`` -- selects the rate variant."""

    source_file: str = ""


class CostBreakdown(BaseModel):
    """Cost in USD, split by what was billed."""

    uncached_input: float = 0.0
    cache_read: float = 0.0
    cache_write: float = 0.0
    output: float = 0.0

    no_cache_equivalent: float = 0.0
    """What these same tokens would have cost with every cache read billed as
    full-price input and no write premium paid -- the baseline for cache savings."""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def total(self) -> float:
        return self.uncached_input + self.cache_read + self.cache_write + self.output

    @computed_field  # type: ignore[prop-decorator]
    @property
    def cache_savings(self) -> float:
        return self.no_cache_equivalent - self.total

    def __add__(self, other: CostBreakdown) -> CostBreakdown:
        return CostBreakdown(
            uncached_input=self.uncached_input + other.uncached_input,
            cache_read=self.cache_read + other.cache_read,
            cache_write=self.cache_write + other.cache_write,
            output=self.output + other.output,
            no_cache_equivalent=self.no_cache_equivalent + other.no_cache_equivalent,
        )


class PricedEvent(BaseModel):
    event: UsageEvent
    cost: CostBreakdown


class Bucket(BaseModel):
    """One row of an aggregation (a day, a model, a project, a tool...)."""

    key: str
    label: str = ""
    tokens: TokenUsage = Field(default_factory=TokenUsage)
    cost: CostBreakdown = Field(default_factory=CostBreakdown)
    events: int = 0
    sessions: int = 0

    def model_post_init(self, _: object) -> None:
        if not self.label:
            self.label = self.key
