---
title: Usage collection
aliases: []
tags: [generated, spec, subdomain]
area: business
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/cli.py, src/ai_usage_cost/collect.py, src/ai_usage_cost/sources/base.py,
  src/ai_usage_cost/store.py, tests/test_collect.py, tests/test_demo.py]
generated: true
---

# Usage collection

> [!info] What this is
> A subdomain: one area of the business that the application serves. This note lists its use cases, the rules it enforces and the terms it uses.

- **Type:** supporting

## Description

Finds the logs and databases that AI coding tools write, parses changed files and keeps one stored request per fingerprint. Main code: [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:190]] and [[src/ai_usage_cost/sources/base.py|src/ai_usage_cost/sources/base.py:18]].

## Use cases (2)

- [[UC-24 Try the tool with demo data]]
- [[UC-25 Sample GPU use for local models]]

## Business rules (6)

All of them, with the code that enforces each one: [[Usage collection Rules]].

- [[Usage collection Rules#BR-119 Schema migrations only run forward|BR-119 Schema migrations only run forward]]
- [[Usage collection Rules#BR-69 A request is stored once per fingerprint|BR-69 A request is stored once per fingerprint]]
- [[Usage collection Rules#BR-70 Records that disagree on input tokens keep the first|BR-70 Records that disagree on input tokens keep the first]]
- [[Usage collection Rules#BR-71 An unchanged file is not parsed again|BR-71 An unchanged file is not parsed again]]
- [[Usage collection Rules#BR-72 A grown file resumes only when its earlier bytes are unchanged|BR-72 A grown file resumes only when its earlier bytes are unchanged]]
- [[Usage collection Rules#BR-86 Source databases are opened read only|BR-86 Source databases are opened read only]]
