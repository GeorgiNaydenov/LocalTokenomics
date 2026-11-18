---
code: OQ-11
priority: medium
status: open
linked:
  - SessionRow
tags:
  - ba/open-question
maturity: draft
---
# Should the series use the local day

## Question

The series groups by the UTC date of an event `src/ai_usage_cost/aggregate.py:544` while every other day view uses the local day `src/ai_usage_cost/models.py:146`. Is that intended?

## Raised by

Reading aggregate.py and models.py
