---
title: Cost pricing
aliases: []
tags: [generated, spec, subdomain]
area: business
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/pricing.py]
generated: true
---

# Cost pricing

> [!info] What this is
> A subdomain: one area of the business that the application serves. This note lists its use cases, the rules it enforces and the terms it uses.

- **Type:** core

## Description

Turns token counts into the cost the same usage would have had at published API list prices, using a rate table with periods, bands, tiers and peak windows. Main code: [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:495]] and [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:252]].

## Business rules (15)

All of them, with the code that enforces each one: [[Cost pricing Rules]].

- [[Cost pricing Rules#BR-54 Missing token counts mean unavailable|BR-54 Missing token counts mean unavailable]]
- [[Cost pricing Rules#BR-55 A free provider costs zero|BR-55 A free provider costs zero]]
- [[Cost pricing Rules#BR-56 A model without a rate row is unpriced|BR-56 A model without a rate row is unpriced]]
- [[Cost pricing Rules#BR-57 A prefix match is an estimate|BR-57 A prefix match is an estimate]]
- [[Cost pricing Rules#BR-58 Only listed suffixes count as the same model|BR-58 Only listed suffixes count as the same model]]
- [[Cost pricing Rules#BR-59 The longest matching row wins|BR-59 The longest matching row wins]]
- [[Cost pricing Rules#BR-60 A known unpriced model beats a guess|BR-60 A known unpriced model beats a guess]]
- [[Cost pricing Rules#BR-61 Duplicate rate keys are rejected|BR-61 Duplicate rate keys are rejected]]
- [[Cost pricing Rules#BR-62 A row must name a defined provider|BR-62 A row must name a defined provider]]
- [[Cost pricing Rules#BR-63 Price periods must not overlap|BR-63 Price periods must not overlap]]
- [[Cost pricing Rules#BR-64 Peak windows must not wrap midnight|BR-64 Peak windows must not wrap midnight]]
- [[Cost pricing Rules#BR-65 The first covering period replaces the row prices|BR-65 The first covering period replaces the row prices]]
- [[Cost pricing Rules#BR-66 The largest band at or under the request size applies|BR-66 The largest band at or under the request size applies]]
- [[Cost pricing Rules#BR-67 An unpriced tier is billed standard and flagged|BR-67 An unpriced tier is billed standard and flagged]]
- [[Cost pricing Rules#BR-68 Cache prices fall back in a fixed order|BR-68 Cache prices fall back in a fixed order]]
