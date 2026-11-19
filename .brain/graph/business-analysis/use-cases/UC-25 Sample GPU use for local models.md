---
code: UC-25
primary_actor: Person using the tool
subdomain: Usage collection
level: subfunction
actors:
  - Person using the tool
models: []
rules: []
tags:
  - ba/use-case
maturity: approved
---
# Sample GPU use for local models

## Description

The person records GPU load and memory while local models run, so energy can be estimated from a power rating.

## Preconditions

A sampler is available: nvidia-smi, rocm-smi or Windows performance counters.

## Postconditions

Samples are stored, and energy is shown when a power rating is given.

## Main flow

1. The person runs the collect command. `src/ai_usage_cost/cli.py:200`
2. The command picks a backend. `src/ai_usage_cost/collect.py:85`
3. Each interval it takes a sample and stores it. `src/ai_usage_cost/collect.py:275`
4. Energy is the rating times utilisation times elapsed time, only when a rating is given. `src/ai_usage_cost/collect.py:255`

## Alternative flows

- With no sampler the command prints that none is available and exits with code 1. `src/ai_usage_cost/cli.py:214`

## Acceptance criteria

- Energy is unavailable without a rating. `tests/test_collect.py:105`
- No rows are written when no backend exists. `tests/test_collect.py:87`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::collect | inferred
  > def collect(
