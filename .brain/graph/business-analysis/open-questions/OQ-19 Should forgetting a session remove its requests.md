---
code: OQ-19
priority: high
status: open
linked:
  - Forget a session
tags:
  - ba/open-question
maturity: draft
---
# Should forgetting a session remove its requests

## Question

Forgetting removes spans and the rating but keeps requests `src/ai_usage_cost/store.py:595`. Should the session's cost and raw records also go, and should project exclusion apply to requests?

## Raised by

Reading store.py and api.py
