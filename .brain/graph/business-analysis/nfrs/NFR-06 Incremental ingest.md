---
code: NFR-06
category: performance
target: An unchanged file is skipped and a grown file is read from its old end when its source allows
applies_to:
  - Usage collection
tags:
  - ba/nfr
maturity: approved
---
# Incremental ingest

## Statement

Ingest avoids reparsing work: it skips unchanged files `src/ai_usage_cost/store.py:229` and hashes a fixed window of `src/ai_usage_cost/store.py:19` bytes to check a resumed file.
