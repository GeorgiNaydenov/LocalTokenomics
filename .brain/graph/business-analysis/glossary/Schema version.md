---
in_application: The number SQLite keeps as user_version, telling which migrations the store has already run (`current` at `src/ai_usage_cost/store.py:146`). The code declares it at `src/ai_usage_cost/store.py:146`, where the line reads `current = conn.execute("PRAGMA user_version").fetchone()[0]`.
tags:
  - ba/glossary-term
maturity: draft
---
# Schema version

## Definition

The number SQLite keeps as user_version, telling which migrations the store has already run. `src/ai_usage_cost/store.py:146`
