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

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/trace.py::_values_match_provenance | inferred
  > if (value is None) != (provenance == "unavailable"):
