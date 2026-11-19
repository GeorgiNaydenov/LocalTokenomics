---
code: NFR-09
category: reliability
target: Journal mode WAL and migrations by user version
applies_to:
  - Usage collection
tags:
  - ba/nfr
maturity: approved
---
# Store uses write ahead logging

## Statement

The store opens in WAL mode and applies pending migrations in order: `src/ai_usage_cost/store.py:144` and `src/ai_usage_cost/store.py:146`.
