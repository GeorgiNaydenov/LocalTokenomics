from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from .models import CostBreakdown, CostState, TokenUsage, UsageEvent

DEFAULT_RATES_PATH = Path(__file__).with_name("rates.json")
MILLION = 1_000_000.0


class RateVariant(BaseModel):
    input: float
    output: float


class ModelRate(BaseModel):
    match: str
    provider: str
    display: str
    input: float
    output: float
    variants: dict[str, RateVariant] = Field(default_factory=dict)

    def for_tier(self, tier: str) -> RateVariant:
        variant = self.variants.get(tier)
        if variant is not None:
            return variant
        return RateVariant(input=self.input, output=self.output)


class ProviderRules(BaseModel):
    cache_read: float = 0.1
    cache_write_5m: float = 1.25
    cache_write_1h: float = 2.0
    batch: float = 0.5
    free: bool = False


class Prefix(BaseModel):
    prefix: str
    provider: str | None = None


class RateTable(BaseModel):
    as_of: str = ""
    currency: str = "USD"
    units: str = ""
    notes: list[str] = Field(default_factory=list)
    prefixes: list[Prefix] = Field(default_factory=list)
    providers: dict[str, ProviderRules] = Field(default_factory=dict)
    models: list[ModelRate] = Field(default_factory=list)

    @classmethod
    def load(cls, path: Path | None = None) -> RateTable:
        return cls.model_validate(json.loads((path or DEFAULT_RATES_PATH).read_text("utf-8")))

    def lookup(self, model: str | None) -> ModelRate | None:
        if not model:
            return None
        name = normalise_model(model, self.prefixes)
        best: ModelRate | None = None
        for rate in self.models:
            if name.startswith(rate.match) and (best is None or len(rate.match) > len(best.match)):
                best = rate
        return best

    def rules_for(self, provider: str) -> ProviderRules:
        return self.providers.get(provider, ProviderRules())

    def display_name(self, model: str | None) -> str:
        rate = self.lookup(model)
        if rate:
            return rate.display
        return model or "unknown model"


def normalise_model(model: str, prefixes: list[Prefix]) -> str:
    name = model.strip().lower()
    for entry in prefixes:
        if name.startswith(entry.prefix):
            name = name[len(entry.prefix) :]
            break
    return name


def resolve_provider(declared: str | None, model: str | None, table: RateTable) -> str:
    if declared:
        return declared
    if model:
        name = model.strip().lower()
        for entry in table.prefixes:
            if name.startswith(entry.prefix) and entry.provider:
                return entry.provider
    rate = table.lookup(model)
    if rate:
        return rate.provider
    return "unknown"


def cost_state_of(
    tokens: TokenUsage | None, provider: str, rate: ModelRate | None, table: RateTable
) -> CostState:
    if table.rules_for(provider).free:
        return "free"
    if tokens is None:
        return "unavailable"
    if rate is None:
        return "unpriced"
    return "priced"


def price_event(event: UsageEvent, table: RateTable) -> tuple[CostBreakdown | None, CostState]:
    provider = resolve_provider(event.provider, event.model, table)
    rate = table.lookup(event.model)
    state = cost_state_of(event.tokens, provider, rate, table)
    if state == "free":
        return CostBreakdown(), "free"
    if state != "priced" or rate is None or event.tokens is None:
        return None, state
    return cost_of(event.tokens, rate, table.rules_for(rate.provider), event.tier), "priced"


def cost_of(
    tokens: TokenUsage,
    rate: ModelRate,
    rules: ProviderRules,
    tier: str = "standard",
) -> CostBreakdown:
    variant = rate.for_tier(tier)
    discount = rules.batch if tier == "batch" else 1.0
    in_price = variant.input * discount / MILLION
    out_price = variant.output * discount / MILLION

    output_cost = tokens.output * out_price
    cache_write_cost = (
        tokens.cache_write_5m * in_price * rules.cache_write_5m
        + tokens.cache_write_1h * in_price * rules.cache_write_1h
    )
    return CostBreakdown(
        uncached_input=tokens.uncached_input * in_price,
        cache_read=tokens.cache_read * in_price * rules.cache_read,
        cache_write=cache_write_cost,
        output=output_cost,
        no_cache_equivalent=tokens.input_total * in_price + output_cost,
    )
