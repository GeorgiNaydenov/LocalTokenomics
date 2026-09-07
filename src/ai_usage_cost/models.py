from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, computed_field

CostState = Literal["priced", "free", "unpriced", "unavailable"]


class TokenUsage(BaseModel):
    uncached_input: int = 0
    cache_read: int = 0
    cache_write_5m: int = 0
    cache_write_1h: int = 0
    output: int = 0
    reasoning_output: int = 0

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
        )


RawScalar = str | int | float | bool | None


class UsageEvent(BaseModel):
    source: str
    client: str
    provider: str | None = None
    model: str | None = None
    timestamp: datetime
    session_id: str
    request_id: str | None = None
    tokens: TokenUsage | None = None
    is_sidechain: bool = False
    tier: str = "standard"
    project: str | None = None
    working_directory: str | None = None
    repository: str | None = None
    branch: str | None = None
    machine: str = ""
    source_file: str = ""
    raw: dict[str, RawScalar] = Field(default_factory=dict)


class CostBreakdown(BaseModel):
    uncached_input: float = 0.0
    cache_read: float = 0.0
    cache_write: float = 0.0
    output: float = 0.0
    no_cache_equivalent: float = 0.0

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
    cost: CostBreakdown | None
    state: CostState


class Bucket(BaseModel):
    key: str
    label: str = ""
    tokens: TokenUsage = Field(default_factory=TokenUsage)
    cost: CostBreakdown = Field(default_factory=CostBreakdown)
    events: int = 0
    sessions: int = 0

    def model_post_init(self, _: object) -> None:
        if not self.label:
            self.label = self.key
