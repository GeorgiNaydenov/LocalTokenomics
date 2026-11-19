---
title: Spend reporting
aliases: []
tags: [generated, spec, subdomain]
area: business
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/aggregate.py, src/ai_usage_cost/api.py, src/ai_usage_cost/cli.py,
  src/ai_usage_cost/models.py, src/ai_usage_cost/pipeline.py, src/ai_usage_cost/render/png.py,
  src/ai_usage_cost/render/terminal.py, src/ai_usage_cost/tui.py, tests/test_api.py,
  tests/test_cli.py, tests/test_pipeline.py, tests/test_store.py]
generated: true
---

# Spend reporting

> [!info] What this is
> A subdomain: one area of the business that the application serves. This note lists its use cases, the rules it enforces and the terms it uses.

- **Type:** core

## Description

Joins priced requests into totals, buckets, sessions, facets and warning groups and presents them on the command line and over HTTP. Main code: [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:166]], [[src/ai_usage_cost/aggregate.py|src/ai_usage_cost/aggregate.py:675]], [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:24]] and [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:198]].

## Use cases (7)

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-19 Export a report as a file]]
- [[UC-20 Be alerted when spend rises]]
- [[UC-21 Inspect and rate one session]]
- [[UC-26 Query the store with SQL]]
- [[UC-27 Browse sessions in the terminal]]

## Business rules (11)

All of them, with the code that enforces each one: [[Spend reporting Rules]].

- [[Spend reporting Rules#BR-116 The alert window ends today|BR-116 The alert window ends today]]
- [[Spend reporting Rules#BR-117 A rise is measured against the window just before|BR-117 A rise is measured against the window just before]]
- [[Spend reporting Rules#BR-118 An alert fires only above the threshold|BR-118 An alert fires only above the threshold]]
- [[Spend reporting Rules#BR-120 A route without a store answers 503|BR-120 A route without a store answers 503]]
- [[Spend reporting Rules#BR-78 The local calendar day decides the day of an event|BR-78 The local calendar day decides the day of an event]]
- [[Spend reporting Rules#BR-79 A session shows its worst cost state|BR-79 A session shows its worst cost state]]
- [[Spend reporting Rules#BR-80 A session title prefers the tool, then the latest|BR-80 A session title prefers the tool, then the latest]]
- [[Spend reporting Rules#BR-81 A reported cost that differs is flagged|BR-81 A reported cost that differs is flagged]]
- [[Spend reporting Rules#BR-82 Old rates raise a warning|BR-82 Old rates raise a warning]]
- [[Spend reporting Rules#BR-84 An alert needs exactly one threshold|BR-84 An alert needs exactly one threshold]]
- [[Spend reporting Rules#BR-85 An unknown session answers 404|BR-85 An unknown session answers 404]]
