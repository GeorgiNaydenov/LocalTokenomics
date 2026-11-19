---
title: Cost pricing Rules
aliases: []
tags: [business, generated, rules, spec]
area: business
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/pricing.py]
generated: true
anchors: true
---

# Cost pricing Rules

> [!info] What this is
> The business rules of the [[Cost pricing]] subdomain, as the code enforces them. Each rule is a heading, so a use case links straight to it, and each names the line of code that enforces it.

## BR-54 Missing token counts mean unavailable

A request whose log carries no token counts has the cost state unavailable. It is never priced as zero and never called free. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:420]]

- **Category:** pricing

Source:
- `cost_state_of`: `if tokens is None:`

## BR-55 A free provider costs zero

A request from a provider marked free gets the state free and a zero cost breakdown, provided its tokens are known. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:434]]

- **Category:** pricing

Source:
- `price_event`: `return CostBreakdown(), "free"`

## BR-56 A model without a rate row is unpriced

A request whose model matches no rate row has the state unpriced. Its tokens are counted and its cost is excluded from totals. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:425]]

- **Category:** pricing

Source:
- `cost_state_of`: `return "unpriced"`

## BR-57 A prefix match is an estimate

When a model id matches a row only through a shorter prefix and a remainder that is not a known suffix, the price is flagged estimated and the pipeline raises a warning. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:313]]

- **Category:** pricing

Source:
- `RateTable.lookup`: `kind = "estimated"`

## BR-58 Only listed suffixes count as the same model

A remainder after a row's match key counts as the same model only when it is a dated snapshot, a context window tag, a version or latest. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:221]]

- **Category:** pricing

Source:
- `_BENIGN_SUFFIX`: `_BENIGN_SUFFIX = re.compile(`

## BR-59 The longest matching row wins

When several rows match a model id, the row with the longest match key is used. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:302]]

- **Category:** pricing

Source:
- `RateTable.lookup`: `len(rate.match) > len(best.match)`

## BR-60 A known unpriced model beats a guess

An unpriced entry at least as specific as the matching row stops a prefix estimate, so a variant of a priced model is not guessed from its parent. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:314]]

- **Category:** pricing

Source:
- `RateTable.lookup`: `An unpriced entry at least as specific as the row`

## BR-61 Duplicate rate keys are rejected

A rate table with two rows that share a match key fails to load. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:276]]

- **Category:** data integrity

Source:
- `RateTable._consistent`: `duplicate model match keys`

## BR-62 A row must name a defined provider

When a rate table defines provider blocks, every row must name one of them, so no row is priced silently with default cache rules. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:282]]

- **Category:** data integrity

Source:
- `RateTable._consistent`: `models reference undefined providers`

## BR-63 Price periods must not overlap

A row whose dated periods overlap is rejected at load, because the first matching period would otherwise decide by file order. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:159]]

- **Category:** data integrity

Source:
- `ModelRate._disjoint_periods`: `overlapping periods`

## BR-64 Peak windows must not wrap midnight

A peak window uses weekdays 0 to 6 and hour ranges with start below end and end at most 24, so a window across midnight must be split in the file. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:59]]

- **Category:** data integrity

Source:
- `Peak._valid_window`: `peak utc_hours ranges must satisfy`

## BR-65 The first covering period replaces the row prices

The first period that covers the request's UTC date replaces the row's own price fields, and only the fields the file wrote. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:449]]

- **Category:** pricing

Source:
- `_period_applied`: `The row's price fields after the first period covering`

## BR-66 The largest band at or under the request size applies

Bands are sorted by minimum input and the last band whose minimum is at or under the request's total input prices the whole request. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:511]]

- **Category:** pricing

Source:
- `cost_of`: `sorted ascending: the last band at or under the request size wins`

## BR-67 An unpriced tier is billed standard and flagged

A service tier other than standard and batch that the row has no price for is billed at the standard price and flagged tier unpriced, which raises a warning. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:526]]

- **Category:** pricing

Source:
- `cost_of`: `tier_unpriced = True`

## BR-68 Cache prices fall back in a fixed order

A cache price is the price set's own figure, else the row's published cache to input ratio times the set's input price, else the provider multiplier times it. [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:486]]

- **Category:** pricing

Source:
- `_cache_price`: `the set's own absolute figure`
