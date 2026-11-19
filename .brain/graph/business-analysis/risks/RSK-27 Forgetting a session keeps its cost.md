---
code: RSK-27
impact: A forgotten session still counts in totals and its raw records stay in the store, while its routes answer 404
likelihood: high whenever a session is forgotten
tags:
  - ba/risk
maturity: draft
---
# Forgetting a session keeps its cost

## Risk

Forgetting deletes only the session's spans and rating `src/ai_usage_cost/store.py:597`, and ingest checks exclusions only for spans `src/ai_usage_cost/store.py:273`, so its requests are kept and stored again.

## Mitigation

Not found in the code. See the open question on forgetting requests.
