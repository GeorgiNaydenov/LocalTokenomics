---
code: UC-24
primary_actor: Person using the tool
subdomain: Usage collection
level: goal
actors:
  - Person using the tool
models:
  - UsageEvent
rules: []
tags:
  - ba/use-case
maturity: approved
---
# Try the tool with demo data

## Description

A new person sees a full dashboard from synthetic logs without exposing their own data.

## Preconditions

None.

## Postconditions

A demo tree and a demo store exist apart from the real ones.

## Main flow

1. The person runs the demo command. `src/ai_usage_cost/cli.py:141`
2. If the demo folder is missing the synthetic logs are generated. `src/ai_usage_cost/cli.py:161`
3. The command says the data is synthetic and that the real store is not touched. `src/ai_usage_cost/cli.py:163`
4. It serves the demo roots with the demo store. `src/ai_usage_cost/cli.py:171`

## Alternative flows

- With the off option the demo tree is deleted and the real logs are served. `src/ai_usage_cost/cli.py:151`

## Acceptance criteria

- The demo store is separate from the real store. `tests/test_demo.py:27`
- The demo shows priced, estimated and unpriced states. `tests/test_demo.py:89`
- Off removes the demo tree and serves real data. `tests/test_demo.py:61`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::demo | inferred
  > def demo(
