---
code: NFR-11
category: security
target: Host 127.0.0.1
applies_to:
  - Spend reporting
tags:
  - ba/nfr
maturity: approved
---
# Server binds to loopback by default

## Statement

The serve and sql commands listen on the loopback address unless told otherwise: `src/ai_usage_cost/cli.py:110`.
