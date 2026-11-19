---
code: UC-17
primary_actor: Person using the tool
subdomain: Spend reporting
level: goal
actors:
  - Person using the tool
  - AI coding tool logs
models:
  - UsageEvent
  - PricedEvent
  - Report
rules:
  - An unchanged file is not parsed again
  - A model without a rate row is unpriced
  - The local calendar day decides the day of an event
  - A bad configuration file gives the defaults
  - A free provider costs zero
  - A known unpriced model beats a guess
  - A prefix match is an estimate
  - A row must name a defined provider
  - A settings file that cannot be loaded is ignored as a whole
  - An unpriced tier is billed standard and flagged
  - Cache prices fall back in a fixed order
  - Duplicate rate keys are rejected
  - Missing token counts mean unavailable
  - Only listed suffixes count as the same model
  - Peak windows must not wrap midnight
  - Price periods must not overlap
  - The first covering period replaces the row prices
  - The largest band at or under the request size applies
  - The longest matching row wins
  - _consistent refuses when duplicates
  - _consistent refuses when missing
  - _consistent validates the model
  - _disjoint_periods refuses when earlier.until is None or (later.from_ or date.min) ‹ ea
  - _disjoint_periods validates the model
  - _ordered refuses when self.from_ is not None and self.until is not None and (
  - _ordered validates the model
  - _sorted_bands validates bands
  - _valid_window refuses when any((not 0 ‹= day ‹= 6 for day in self.weekdays))
  - _valid_window refuses when any((not 0 ‹= start ‹ end ‹= 24 for start, end in self
  - _valid_window validates the model
  - read_content refuses when config.metadata_only or span.content_path is None
  - resolve_path refuses when index ›= len(current)
tags:
  - ba/use-case
maturity: approved
---
# See what my AI usage would cost

## Description

The person runs one command and sees what the usage of all their AI coding tools would have cost at list prices, by model, client, provider, project or day.

## Preconditions

At least one supported tool has written logs on the machine, or the person points to them with a root option.

## Postconditions

A report is printed or returned as JSON. The store holds the parsed requests for the next run.

## Main flow

1. The person runs the scan command, which accepts since, until, source, by, json, root, db, rates and rebuild options. `src/ai_usage_cost/cli.py:72`
2. The command analyses the logs. `src/ai_usage_cost/cli.py:87`
3. The analysis loads the privacy settings and opens the store. `src/ai_usage_cost/pipeline.py:175`
4. Changed files are ingested into the store. `src/ai_usage_cost/pipeline.py:178`
5. Stored requests are loaded and each is priced against the rate table. `src/ai_usage_cost/pipeline.py:198`
6. The report is filtered by the dates and sources. `src/ai_usage_cost/cli.py:88`
7. With the json option the report is printed as JSON. `src/ai_usage_cost/cli.py:96`
8. Otherwise the terminal tables are printed. `src/ai_usage_cost/cli.py:105`

## Alternative flows

- When the report has no requests the command prints that no usage was found and exits with code 1. `src/ai_usage_cost/cli.py:104`
- A model with no rate is listed as unpriced and left out of the total. `src/ai_usage_cost/render/terminal.py:34`

## Acceptance criteria

- Since and until include their boundary days. `tests/test_pipeline.py:71`
- Every breakdown sums to the grand total. `tests/test_pipeline.py:203`
- Unavailable and unpriced requests count but do not add cost. `tests/test_pipeline.py:486`
- Scanning twice changes nothing. `tests/test_store.py:158`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/cli.py::scan | inferred
  > def scan(
