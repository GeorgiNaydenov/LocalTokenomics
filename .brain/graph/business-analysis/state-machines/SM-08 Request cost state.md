---
code: SM-08
entity: PricedEvent
tags:
  - ba/state-machine
maturity: approved
---
# Request cost state

## States

| Name |
| --- |
| - priced |
| - free |
| - unpriced |
| - unavailable |
| Each request ends in exactly one state. The estimated flag is a mark on priced, not a state. `src/ai_usage_cost/models.py:8` |

## Transitions

| From | To | Trigger | Code |
|---|---|---|---|
| loaded | unavailable | the request has no token counts | `src/ai_usage_cost/pricing.py:421` |
| loaded | free | the provider rules say free | `src/ai_usage_cost/pricing.py:422` |
| loaded | unpriced | no rate row matches the model | `src/ai_usage_cost/pricing.py:425` |
| loaded | priced | a rate row matches | `src/ai_usage_cost/pricing.py:426` |

| Transitions out of a state are not found: the state is recomputed on every analysis and never changes in place. |

## Sources

- [[Code of localtokenomics]] | inferred
  > def cost_state_of(
