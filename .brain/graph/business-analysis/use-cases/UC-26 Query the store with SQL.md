---
code: UC-26
primary_actor: Person using the tool
subdomain: Spend reporting
level: subfunction
actors:
  - Person using the tool
models: []
rules: []
tags:
  - ba/use-case
maturity: draft
---
# Query the store with SQL

## Description

The person explores the stored requests with SQL in a browser through Datasette.

## Preconditions

The sql extra is installed and a store exists.

## Postconditions

Datasette serves the store.

## Main flow

1. The person runs the sql command. `src/ai_usage_cost/cli.py:229`
2. The command needs Datasette. `src/ai_usage_cost/cli.py:235`
3. It checks that the store file exists. `src/ai_usage_cost/cli.py:239`
4. It hands the store to Datasette. `src/ai_usage_cost/cli.py:248`

## Alternative flows

- A missing store prints a hint and exits with code 2. `src/ai_usage_cost/cli.py:241`

## Acceptance criteria

- The explicit store is handed to Datasette. `tests/test_cli.py:219`
- A missing store is named instead of launching. `tests/test_cli.py:241`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::sql | inferred
  > def sql(
