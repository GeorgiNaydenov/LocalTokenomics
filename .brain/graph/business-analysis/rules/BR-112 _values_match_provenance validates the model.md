---
code: BR-112
category: validator
tags:
  - ba/rule
maturity: approved
---
# _values_match_provenance validates the model

## Statement

In _values_match_provenance, the model: the code validates before accepting the value. Located at src/ai_usage_cost/trace.py lines 89-101.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/trace.py::_values_match_provenance | inferred
  > def _values_match_provenance(self) -> Span:
