---
code: BR-113
category: guard
tags:
  - ba/rule
maturity: approved
---
# _values_match_provenance refuses when (value is None) != (provenance == 'unavailable')

## Statement

In _values_match_provenance, when (value is None) != (provenance == 'unavailable'): the code raises ValueError. Located at src/ai_usage_cost/trace.py lines 96-100.

## Enforced in

- [[UC-13 Discover AI tool usage from local files]]
- [[UC-14 Read a tool's SQLite store without a token count]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/trace.py::_values_match_provenance | inferred
  > if (value is None) != (provenance == "unavailable"):
