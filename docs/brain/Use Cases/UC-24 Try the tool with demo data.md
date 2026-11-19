---
title: UC-24 Try the tool with demo data
aliases: [UC-24, Try the tool with demo data]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/cli.py, tests/test_demo.py]
generated: true
use-cases: [UC-24]
subdomain: Usage collection
---

# UC-24 Try the tool with demo data

> [!info] What this is
> A use case of the [[Usage collection]] subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Subdomain:** [[Usage collection]]
- **Actors:** [[Actors#Person using the tool|Person using the tool]], [[Actors|UsageEvent]]
- **Maturity:** approved

## Description

A new person sees a full dashboard from synthetic logs without exposing their own data.

## Preconditions

None.

## Main flow

1. The person runs the demo command. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:141]]
2. If the demo folder is missing the synthetic logs are generated. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:161]]
3. The command says the data is synthetic and that the real store is not touched. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:163]]
4. It serves the demo roots with the demo store. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:171]]

## Alternative flows

- With the off option the demo tree is deleted and the real logs are served. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:151]]

## Postconditions

A demo tree and a demo store exist apart from the real ones.

## Acceptance criteria

- The demo store is separate from the real store. [[tests/test_demo.py|tests/test_demo.py:27]]
- The demo shows priced, estimated and unpriced states. [[tests/test_demo.py|tests/test_demo.py:89]]
- Off removes the demo tree and serves real data. [[tests/test_demo.py|tests/test_demo.py:61]]

## Code

- [[src/ai_usage_cost/cli.py]]
- [[tests/test_demo.py]]
