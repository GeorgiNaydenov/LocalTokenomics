"""Rate table loading and cost arithmetic.

The table lives in ``rates.json`` next to this module and is plain data -- nothing is
fetched at runtime. Unknown models are never silently priced at zero: they are collected
on the :class:`Pricer` so the CLI and API can report them.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from pydantic import BaseModel, Field

from .models import CostBreakdown, TokenUsage, UsageEvent

DEFAULT_RATES_PATH = Path(__file__).with_name("rates.json")
MILLION = 1_000_000.0

# Provider prefixes seen in logs that are not part of the model identity.
_STRIP_PREFIXES = ("anthropic/", "openai/", "us.anthropic.", "eu.anthropic.", "openrouter/")


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


class RateTable(BaseModel):
    as_of: str = ""
    currency: str = "USD"
    units: str = ""
    notes: list[str] = Field(default_factory=list)
    providers: dict[str, ProviderRules] = Field(default_factory=dict)
    models: list[ModelRate] = Field(default_factory=list)

    @classmethod
    def load(cls, path: Path | None = None) -> RateTable:
        return cls.model_validate(json.loads((path or DEFAULT_RATES_PATH).read_text("utf-8")))

    def lookup(self, model: str) -> ModelRate | None:
        """Longest-prefix match, so dated snapshots resolve to their family."""
        name = normalise_model(model)
        best: ModelRate | None = None
        for rate in self.models:
            if name.startswith(rate.match) and (best is None or len(rate.match) > len(best.match)):
                best = rate
        return best

    def rules_for(self, provider: str) -> ProviderRules:
        return self.providers.get(provider, ProviderRules())


def normalise_model(model: str) -> str:
    name = model.strip().lower()
    for prefix in _STRIP_PREFIXES:
        if name.startswith(prefix):
            name = name[len(prefix) :]
    return name


class Pricer:
    """Prices :class:`UsageEvent` objects and remembers what it could not price."""

    def __init__(self, table: RateTable | None = None) -> None:
        self.table = table or RateTable.load()
        self.unknown_models: dict[str, TokenUsage] = defaultdict(TokenUsage)
        self.unknown_events: dict[str, int] = defaultdict(int)

    def price(self, event: UsageEvent) -> CostBreakdown | None:
        rate = self.table.lookup(event.model)
        if rate is None:
            self.unknown_models[event.model] = self.unknown_models[event.model] + event.tokens
            self.unknown_events[event.model] += 1
            return None
        return cost_of(event.tokens, rate, self.table.rules_for(rate.provider), event.tier)

    def display_name(self, model: str) -> str:
        rate = self.table.lookup(model)
        return rate.display if rate else model

    def provider_of(self, model: str) -> str:
        rate = self.table.lookup(model)
        return rate.provider if rate else "unknown"


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
        # Same tokens, no cache: every input token billed at the full input rate.
        no_cache_equivalent=tokens.input_total * in_price + output_cost,
    )
