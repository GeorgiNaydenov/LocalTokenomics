---
title: UC-17 See what my AI usage would cost
aliases: [UC-17, See what my AI usage would cost]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/cli.py, src/ai_usage_cost/pipeline.py, src/ai_usage_cost/render/terminal.py,
  tests/test_pipeline.py, tests/test_store.py]
generated: true
use-cases: [UC-17]
subdomain: Spend reporting
---

# UC-17 See what my AI usage would cost

> [!info] What this is
> A use case of the [[Spend reporting]] subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Subdomain:** [[Spend reporting]]
- **Actors:** [[Actors|A model without a rate row is unpriced]], [[Actors#AI coding tool logs|AI coding tool logs]], [[Actors|An unchanged file is not parsed again]], [[Actors#Person using the tool|Person using the tool]], [[Actors|PricedEvent]], [[Actors|Report]], [[Actors|The local calendar day decides the day of an event]], [[Actors|UsageEvent]]
- **Maturity:** approved

## Description

The person runs one command and sees what the usage of all their AI coding tools would have cost at list prices, by model, client, provider, project or day.

## Preconditions

At least one supported tool has written logs on the machine, or the person points to them with a root option.

## Main flow

1. The person runs the scan command, which accepts since, until, source, by, json, root, db, rates and rebuild options. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:72]]
2. The command analyses the logs. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:87]]
3. The analysis loads the privacy settings and opens the store. [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:175]]
4. Changed files are ingested into the store. [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:178]]
5. Stored requests are loaded and each is priced against the rate table. [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:198]]
6. The report is filtered by the dates and sources. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:88]]
7. With the json option the report is printed as JSON. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:96]]
8. Otherwise the terminal tables are printed. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:105]]

## Alternative flows

- When the report has no requests the command prints that no usage was found and exits with code 1. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:104]]
- A model with no rate is listed as unpriced and left out of the total. [[src/ai_usage_cost/render/terminal.py|src/ai_usage_cost/render/terminal.py:34]]

## Postconditions

A report is printed or returned as JSON. The store holds the parsed requests for the next run.

## Acceptance criteria

- Since and until include their boundary days. [[tests/test_pipeline.py|tests/test_pipeline.py:71]]
- Every breakdown sums to the grand total. [[tests/test_pipeline.py|tests/test_pipeline.py:203]]
- Unavailable and unpriced requests count but do not add cost. [[tests/test_pipeline.py|tests/test_pipeline.py:486]]
- Scanning twice changes nothing. [[tests/test_store.py|tests/test_store.py:158]]

## Business rules

- [[Spend reporting Rules#BR-116 The alert window ends today|BR-116 The alert window ends today]]
- [[Spend reporting Rules#BR-117 A rise is measured against the window just before|BR-117 A rise is measured against the window just before]]
- [[Spend reporting Rules#BR-118 An alert fires only above the threshold|BR-118 An alert fires only above the threshold]]
- [[Spend reporting Rules#BR-81 A reported cost that differs is flagged|BR-81 A reported cost that differs is flagged]]
- [[Spend reporting Rules#BR-82 Old rates raise a warning|BR-82 Old rates raise a warning]]
- [[Spend reporting Rules#BR-84 An alert needs exactly one threshold|BR-84 An alert needs exactly one threshold]]

## Code

- [[src/ai_usage_cost/cli.py]]
- [[src/ai_usage_cost/pipeline.py]]
- [[src/ai_usage_cost/render/terminal.py]]
- [[tests/test_pipeline.py]]
- [[tests/test_store.py]]
