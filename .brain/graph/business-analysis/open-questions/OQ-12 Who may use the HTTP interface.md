---
code: OQ-12
priority: medium
status: open
linked:
  - Person using the tool
tags:
  - ba/open-question
maturity: approved
---
# Who may use the HTTP interface

## Question

The code has no caller check `src/ai_usage_cost/api.py:198`. Is loopback binding the intended only control, and is a non loopback host a supported setup?

## Raised by

Reading api.py and cli.py
