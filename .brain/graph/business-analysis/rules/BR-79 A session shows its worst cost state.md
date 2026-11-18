---
code: BR-79
category: reporting
subdomain: Spend reporting
tags:
  - ba/rule
maturity: draft
---
# A session shows its worst cost state

## Statement

The cost state of a session is the worst of its requests, ranked priced, free, unpriced, unavailable. `src/ai_usage_cost/aggregate.py:640`

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/aggregate.py::sessions_of | inferred
  > row.cost_state = max(states[key], key=lambda s: _STATE_RANK[s])
