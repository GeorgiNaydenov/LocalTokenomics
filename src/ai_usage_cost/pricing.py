from __future__ import annotations

import json
import re
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Literal

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    computed_field,
    field_validator,
    model_validator,
)

from .models import CostBreakdown, CostState, TokenUsage, UsageEvent

DEFAULT_RATES_PATH = Path(__file__).with_name("rates.json")
MILLION = 1_000_000.0

MatchKind = Literal["exact", "suffix", "estimated"]
RowStatus = Literal["ga", "preview", "retired"]


class PriceSet(BaseModel):
    """One set of USD-per-million prices. Cache fields are absolute figures as published;
    None means "not published for this set" and is derived at cost time (see `cost_of`)."""

    input: float
    output: float
    cache_read: float | None = None
    cache_write_5m: float | None = None
    cache_write_1h: float | None = None


class Band(PriceSet):
    """Whole-request price once a request's total input reaches `min_input_tokens`."""

    min_input_tokens: int
    variants: dict[str, PriceSet] | None = None


class Peak(PriceSet):
    """A recurring UTC window (weekday set + half-open hour ranges) with its own price."""

    weekdays: list[int] = Field(default_factory=list)
    utc_hours: list[tuple[int, int]] = Field(default_factory=list)

    @model_validator(mode="after")
    def _valid_window(self) -> Peak:
        if any(not 0 <= day <= 6 for day in self.weekdays):
            raise ValueError("peak weekdays must be 0 (Monday) to 6 (Sunday)")
        # A wrap-around range such as [22, 2] would silently never match, so split it in the file.
        if any(not 0 <= start < end <= 24 for start, end in self.utc_hours):
            raise ValueError("peak utc_hours ranges must satisfy 0 <= start < end <= 24")
        return self

    def covers(self, when: datetime) -> bool:
        if when.weekday() not in self.weekdays:
            return False
        return any(start <= when.hour < end for start, end in self.utc_hours)


class Period(BaseModel):
    """An effective-dated override of the row's top-level price fields.

    Only fields the file actually wrote replace the row's value (tracked through
    `model_fields_set`), so an explicit `null` cache price is distinguishable from an
    omitted one.
    """

    model_config = ConfigDict(populate_by_name=True)

    from_: date | None = Field(default=None, alias="from")
    until: date | None = None
    input: float | None = None
    output: float | None = None
    cache_read: float | None = None
    cache_write_5m: float | None = None
    cache_write_1h: float | None = None
    variants: dict[str, PriceSet] | None = None
    bands: list[Band] | None = None
    peak: Peak | None = None

    @model_validator(mode="after")
    def _ordered(self) -> Period:
        if self.from_ is not None and self.until is not None and self.from_ >= self.until:
            raise ValueError("period `from` must be earlier than `until`")
        return self

    def covers(self, day: date) -> bool:
        return (self.from_ is None or self.from_ <= day) and (
            self.until is None or day < self.until
        )


class ProviderRules(BaseModel):
    cache_read: float = 0.1
    cache_write_5m: float = 1.25
    cache_write_1h: float = 2.0
    batch: float = 0.5
    free: bool = False


class PartialRules(BaseModel):
    """A per-model `cache_rules` override: every field optional, merged over the provider
    block so an omitted field keeps the provider's value instead of a class default."""

    cache_read: float | None = None
    cache_write_5m: float | None = None
    cache_write_1h: float | None = None
    batch: float | None = None
    free: bool | None = None


def merge_rules(base: ProviderRules, override: PartialRules | None) -> ProviderRules:
    if override is None:
        return base
    return ProviderRules(**{**base.model_dump(), **override.model_dump(exclude_none=True)})


class ModelRate(PriceSet):
    match: str
    provider: str
    display: str
    variants: dict[str, PriceSet] = Field(default_factory=dict)
    bands: list[Band] = Field(default_factory=list)
    peak: Peak | None = None
    periods: list[Period] = Field(default_factory=list)
    cache_rules: PartialRules | None = None
    context_window: int | None = None
    source: str | None = None
    verified: date | None = None
    status: RowStatus = "ga"
    released: date | None = None
    retired: date | None = None
    note: str | None = None
    # Set by `RateTable.lookup` on the returned copy, never read from a file: True when the
    # model id only prefix-matched this row without a benign suffix.
    estimated: bool = Field(default=False, validation_alias=AliasChoices("estimated", "inherited"))
    match_kind: MatchKind | None = None

    @field_validator("bands")
    @classmethod
    def _sorted_bands(cls, bands: list[Band]) -> list[Band]:
        return sorted(bands, key=lambda band: band.min_input_tokens)

    @model_validator(mode="after")
    def _disjoint_periods(self) -> ModelRate:
        # The first matching period wins at cost time, so an overlap would be priced by file
        # order alone. Reject it at load instead of letting a bad file price quietly.
        bounded = sorted(self.periods, key=lambda period: period.from_ or date.min)
        for earlier, later in zip(bounded, bounded[1:], strict=False):
            if earlier.until is None or (later.from_ or date.min) < earlier.until:
                raise ValueError(f"{self.match}: overlapping periods")
        return self

    @computed_field  # type: ignore[prop-decorator]
    @property
    def inherited(self) -> bool:
        """Read-only alias of `estimated`, kept so existing JSON consumers keep working."""
        return self.estimated


class Prefix(BaseModel):
    prefix: str
    provider: str | None = None


# Gateway prefixes understood even when rates.json lists none. File entries with the same
# prefix win. Matching is longest-first and repeated, so `us.anthropic.` beats `anthropic.`
# and `openrouter/anthropic/<id>` loses both.
BUILTIN_PREFIXES: list[Prefix] = [
    Prefix(prefix="global.anthropic.", provider="bedrock"),
    Prefix(prefix="apac.anthropic.", provider="bedrock"),
    Prefix(prefix="us.anthropic.", provider="bedrock"),
    Prefix(prefix="eu.anthropic.", provider="bedrock"),
    Prefix(prefix="au.anthropic.", provider="bedrock"),
    Prefix(prefix="jp.anthropic.", provider="bedrock"),
    Prefix(prefix="anthropic."),
    Prefix(prefix="openrouter/", provider="openrouter"),
    Prefix(prefix="azure/", provider="azure"),
    Prefix(prefix="anthropic/"),
    Prefix(prefix="openai/"),
    Prefix(prefix="google/"),
    Prefix(prefix="models/"),
    Prefix(prefix="vertex_ai/"),
    Prefix(prefix="x-ai/"),
    Prefix(prefix="xai/"),
    Prefix(prefix="meta/"),
    Prefix(prefix="typesafe/"),
    Prefix(prefix="moonshotai/"),
    Prefix(prefix="deepseek/"),
    Prefix(prefix="mistralai/"),
    Prefix(prefix="github-copilot/"),
    Prefix(prefix="copilot/"),
    Prefix(prefix="kilo/"),
    Prefix(prefix="opencode/"),
    Prefix(prefix="qwen/"),
    Prefix(prefix="z-ai/"),
    Prefix(prefix="zhipu/"),
    Prefix(prefix="alibaba/"),
    Prefix(prefix="moonshot/"),
    Prefix(prefix="amazon/"),
    Prefix(prefix="minimax/"),
    Prefix(prefix="global.amazon.", provider="bedrock"),
    Prefix(prefix="apac.amazon.", provider="bedrock"),
    Prefix(prefix="us.amazon.", provider="bedrock"),
    Prefix(prefix="eu.amazon.", provider="bedrock"),
    Prefix(prefix="amazon.", provider="bedrock"),
]

# The only remainders after a row's `match` that still count as the same model: a dated
# snapshot, a context-window tag, a Bedrock version, or a `-latest` alias. Anything else
# (`-mini`, `-5`, `.7`, `:free`, `-preview`) is a different model priced as a guess.
_BENIGN_TOKEN = r"(?:-\d{8}|-\d{4}-\d{2}-\d{2}|@\d{8}|\[1m\]|-v\d+(?::\d+)?|-latest)"
_BENIGN_SUFFIX = re.compile(f"{_BENIGN_TOKEN}+")


class ModelMatch(BaseModel):
    """How one raw model id resolved against the rate table: the row's `match` key (None
    when unpriced) and the match kind, so a UI can join spend to rate rows by key."""

    match: str | None = None
    kind: Literal["exact", "suffix", "estimated", "none"] = "none"


class UnpricedModel(BaseModel):
    """A model id that is known but has no published per-token rate.

    Distinct from a model rates.json has simply never heard of: this is an
    explicit acknowledgement (with `note` explaining why) so the UI can say
    *why* a real, named model is unpriced instead of implying it was missed.
    """

    match: str
    note: str
    status: Literal["watchlist", "no_list_price"] | None = None


def effective_prefixes(file_prefixes: list[Prefix]) -> list[Prefix]:
    """Built-in gateway prefixes merged with the file's (file wins), longest first."""
    merged = {entry.prefix: entry for entry in BUILTIN_PREFIXES}
    merged.update({entry.prefix: entry for entry in file_prefixes})
    return sorted(merged.values(), key=lambda entry: len(entry.prefix), reverse=True)


class RateTable(BaseModel):
    as_of: str = ""
    currency: str = "USD"
    units: str = ""
    notes: list[str] = Field(default_factory=list)
    prefixes: list[Prefix] = Field(default_factory=list)
    providers: dict[str, ProviderRules] = Field(default_factory=dict)
    models: list[ModelRate] = Field(default_factory=list)
    unpriced_models: list[UnpricedModel] = Field(default_factory=list)

    # `lookup()` is called once per priced span -- tens of thousands of times for one large
    # session -- and does a linear prefix scan over every rate entry. Sessions are dominated
    # by a handful of distinct model strings, so caching by the raw (pre-normalised) model
    # name collapses that scan to one per distinct model actually seen. A private attribute,
    # not a field: it must never be serialized, diffed, or treated as part of the rate data.
    _lookup_cache: dict[str, ModelRate | None] = PrivateAttr(default_factory=dict)
    _rules_cache: dict[str, ProviderRules] = PrivateAttr(default_factory=dict)
    _prefix_cache: list[Prefix] | None = PrivateAttr(default=None)

    @model_validator(mode="after")
    def _consistent(self) -> RateTable:
        keys = [rate.match for rate in self.models]
        duplicates = sorted({key for key in keys if keys.count(key) > 1})
        if duplicates:
            raise ValueError(f"duplicate model match keys: {', '.join(duplicates)}")
        if self.providers:
            # A row whose provider has no block would silently price its cache with the
            # Anthropic-shaped class defaults.
            missing = sorted({rate.provider for rate in self.models} - set(self.providers))
            if missing:
                raise ValueError(f"models reference undefined providers: {', '.join(missing)}")
        return self

    @classmethod
    def load(cls, path: Path | None = None) -> RateTable:
        return cls.model_validate(json.loads((path or DEFAULT_RATES_PATH).read_text("utf-8")))

    def all_prefixes(self) -> list[Prefix]:
        if self._prefix_cache is None:
            self._prefix_cache = effective_prefixes(self.prefixes)
        return self._prefix_cache

    def lookup(self, model: str | None) -> ModelRate | None:
        if not model:
            return None
        if model in self._lookup_cache:
            return self._lookup_cache[model]
        name = normalise_model(model, self.all_prefixes())
        best: ModelRate | None = None
        for rate in self.models:
            if name.startswith(rate.match) and (best is None or len(rate.match) > len(best.match)):
                best = rate
        result: ModelRate | None = None
        if best is not None:
            remainder = name[len(best.match) :]
            kind: MatchKind
            if not remainder:
                kind = "exact"
            elif _BENIGN_SUFFIX.fullmatch(remainder):
                kind = "suffix"
            else:
                kind = "estimated"
            # An unpriced entry at least as specific as the row (e.g. a `-spark` variant of a
            # priced model) beats a guess from the parent; an exact or suffix match on a real
            # row always wins over it.
            if kind != "estimated" or not self._unpriced_covers(name, len(best.match)):
                result = best.model_copy(
                    update={"match_kind": kind, "estimated": kind == "estimated"}
                )
        self._lookup_cache[model] = result
        return result

    def _unpriced_covers(self, name: str, matched_len: int) -> bool:
        return any(
            name.startswith(entry.match) and len(entry.match) >= matched_len
            for entry in self.unpriced_models
        )

    def rules_for(self, provider: str) -> ProviderRules:
        return self.providers.get(provider, ProviderRules())

    def rules_of(self, rate: ModelRate) -> ProviderRules:
        """The provider block with the row's partial `cache_rules` merged over it."""
        cached = self._rules_cache.get(rate.match)
        if cached is None:
            cached = merge_rules(self.rules_for(rate.provider), rate.cache_rules)
            self._rules_cache[rate.match] = cached
        return cached

    def match_of(self, model: str | None) -> ModelMatch:
        rate = self.lookup(model)
        if rate is None or rate.match_kind is None:
            return ModelMatch()
        return ModelMatch(match=rate.match, kind=rate.match_kind)

    def display_name(self, model: str | None) -> str:
        rate = self.lookup(model)
        if rate is not None and rate.match_kind != "estimated":
            return rate.display
        return model or "unknown model"

    def unpriced_note(self, model: str | None) -> str | None:
        """The explanation for a model that is explicitly known to have no rate."""
        if not model:
            return None
        name = normalise_model(model, self.all_prefixes())
        best: UnpricedModel | None = None
        for entry in self.unpriced_models:
            if name.startswith(entry.match) and (
                best is None or len(entry.match) > len(best.match)
            ):
                best = entry
        return best.note if best else None

    def age_days(self, today: date | None = None) -> int | None:
        """Days between `as_of` and `today`; None when `as_of` is empty or unparsable."""
        try:
            stamp = date.fromisoformat(self.as_of)
        except ValueError:
            return None
        return ((today or date.today()) - stamp).days


def _longest_prefix(name: str, prefixes: list[Prefix]) -> Prefix | None:
    best: Prefix | None = None
    for entry in prefixes:
        if entry.prefix and name.startswith(entry.prefix):
            if best is None or len(entry.prefix) > len(best.prefix):
                best = entry
    return best


def normalise_model(model: str, prefixes: list[Prefix]) -> str:
    name = model.strip().lower()
    while True:
        found = _longest_prefix(name, prefixes)
        if found is None:
            break
        name = name[len(found.prefix) :]
    # Gateways and some CLIs write Claude ids with dots (`claude-sonnet-4.6`) where the
    # rows use dashes. Claude only: gpt-5.6, gemini-3.1, glm-4.7 keep theirs.
    if name.startswith("claude-"):
        name = name.replace(".", "-")
    return name


def resolve_provider(declared: str | None, model: str | None, table: RateTable) -> str:
    if declared:
        return declared
    if model:
        name = model.strip().lower()
        prefixes = table.all_prefixes()
        while True:
            found = _longest_prefix(name, prefixes)
            if found is None:
                break
            if found.provider:
                return found.provider
            name = name[len(found.prefix) :]
    rate = table.lookup(model)
    if rate:
        return rate.provider
    return "unknown"


def cost_state_of(
    tokens: TokenUsage | None, provider: str, rate: ModelRate | None, table: RateTable
) -> CostState:
    if tokens is None:
        return "unavailable"
    if table.rules_for(provider).free:
        return "free"
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
    return cost_of(event.tokens, rate, table.rules_of(rate), event.tier, event.timestamp), "priced"


def _utc(stamp: datetime | None) -> datetime:
    if stamp is None:
        return datetime.now(UTC)
    return stamp.astimezone(UTC) if stamp.tzinfo is not None else stamp.replace(tzinfo=UTC)


def _period_applied(
    rate: ModelRate, day: date
) -> tuple[PriceSet, dict[str, PriceSet], list[Band], Peak | None]:
    """The row's price fields after the first period covering `day` replaced its own."""
    for period in rate.periods:
        if not period.covers(day):
            continue
        written = period.model_fields_set
        price = PriceSet(
            input=period.input if period.input is not None else rate.input,
            output=period.output if period.output is not None else rate.output,
            cache_read=period.cache_read if "cache_read" in written else rate.cache_read,
            cache_write_5m=(
                period.cache_write_5m if "cache_write_5m" in written else rate.cache_write_5m
            ),
            cache_write_1h=(
                period.cache_write_1h if "cache_write_1h" in written else rate.cache_write_1h
            ),
        )
        return (
            price,
            period.variants if period.variants is not None else rate.variants,
            (
                sorted(period.bands, key=lambda band: band.min_input_tokens)
                if period.bands is not None
                else rate.bands
            ),
            period.peak if period.peak is not None else rate.peak,
        )
    return rate, rate.variants, rate.bands, rate.peak


def _cache_price(
    published: float | None,
    row_published: float | None,
    row_input: float,
    in_price: float,
    multiplier: float,
    scale: float,
) -> float:
    """USD per token: the set's own absolute figure; else the row's published cache/input
    ratio times this set's input; else the provider multiplier times this set's input."""
    if published is not None:
        return published * scale / MILLION
    if row_published is not None and row_input > 0:
        return row_published / row_input * in_price
    return in_price * multiplier


def cost_of(
    tokens: TokenUsage,
    rate: ModelRate,
    rules: ProviderRules,
    tier: str = "standard",
    timestamp: datetime | None = None,
) -> CostBreakdown:
    """Price one request: period (by UTC date) -> band (by total input) -> service tier ->
    peak window (by UTC weekday/hour) -> cache-price resolution. `timestamp` defaults to now."""
    when = _utc(timestamp)
    price, variants, bands, peak = _period_applied(rate, when.date())

    selected: Band | None = None
    for band in bands:
        if band.min_input_tokens > tokens.input_total:
            break
        selected = band  # sorted ascending: the last band at or under the request size wins
    if selected is not None:
        price = selected
        if selected.variants is not None:
            variants = selected.variants

    discount = 1.0
    tier_unpriced = False
    if tier and tier != "standard":
        variant = variants.get(tier)
        if variant is not None:
            price = variant
        elif tier == "batch":
            discount = rules.batch
        else:
            tier_unpriced = True

    if peak is not None and peak.covers(when):
        price = peak

    in_price = price.input * discount / MILLION
    out_price = price.output * discount / MILLION
    cache_read_price = _cache_price(
        price.cache_read, rate.cache_read, rate.input, in_price, rules.cache_read, discount
    )
    write_5m_price = _cache_price(
        price.cache_write_5m,
        rate.cache_write_5m,
        rate.input,
        in_price,
        rules.cache_write_5m,
        discount,
    )
    write_1h_price = _cache_price(
        price.cache_write_1h,
        rate.cache_write_1h,
        rate.input,
        in_price,
        rules.cache_write_1h,
        discount,
    )

    output_cost = tokens.output * out_price
    return CostBreakdown(
        uncached_input=tokens.uncached_input * in_price,
        cache_read=tokens.cache_read * cache_read_price,
        cache_write=tokens.cache_write_5m * write_5m_price + tokens.cache_write_1h * write_1h_price,
        output=output_cost,
        no_cache_equivalent=tokens.input_total * in_price + output_cost,
        estimated=rate.estimated,
        tier_unpriced=tier_unpriced,
    )
