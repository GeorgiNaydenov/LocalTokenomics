---
code: NFR-07
category: performance
target: One prefix scan per distinct model id
applies_to:
  - Cost pricing
tags:
  - ba/nfr
maturity: approved
---
# Rate lookup is cached

## Statement

Rate lookups are cached by the raw model id because a session calls them tens of thousands of times: `src/ai_usage_cost/pricing.py:267`.
