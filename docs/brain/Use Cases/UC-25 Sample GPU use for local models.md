---
title: UC-25 Sample GPU use for local models
aliases: [UC-25, Sample GPU use for local models]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/cli.py, src/ai_usage_cost/collect.py, tests/test_collect.py]
generated: true
use-cases: [UC-25]
subdomain: Usage collection
---

# UC-25 Sample GPU use for local models

> [!info] What this is
> A use case of the [[Usage collection]] subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Subdomain:** [[Usage collection]]
- **Actors:** [[Actors#Person using the tool|Person using the tool]]
- **Maturity:** approved

## Description

The person records GPU load and memory while local models run, so energy can be estimated from a power rating.

## Preconditions

A sampler is available: nvidia-smi, rocm-smi or Windows performance counters.

## Main flow

1. The person runs the collect command. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:200]]
2. The command picks a backend. [[src/ai_usage_cost/collect.py|src/ai_usage_cost/collect.py:85]]
3. Each interval it takes a sample and stores it. [[src/ai_usage_cost/collect.py|src/ai_usage_cost/collect.py:275]]
4. Energy is the rating times utilisation times elapsed time, only when a rating is given. [[src/ai_usage_cost/collect.py|src/ai_usage_cost/collect.py:255]]

## Alternative flows

- With no sampler the command prints that none is available and exits with code 1. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:214]]

## Postconditions

Samples are stored, and energy is shown when a power rating is given.

## Acceptance criteria

- Energy is unavailable without a rating. [[tests/test_collect.py|tests/test_collect.py:105]]
- No rows are written when no backend exists. [[tests/test_collect.py|tests/test_collect.py:87]]

## Code

- [[src/ai_usage_cost/cli.py]]
- [[src/ai_usage_cost/collect.py]]
- [[tests/test_collect.py]]
