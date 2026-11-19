---
code: BR-103
category: guard
tags:
  - ba/rule
maturity: approved
---
# _ordered refuses when self.from_ is not None and self.until is not None and (

## Statement

In _ordered, when self.from_ is not None and self.until is not None and (self.from_ >= self.until): the code raises ValueError, message "period `from` must be earlier than `until`". Located at src/ai_usage_cost/pricing.py lines 91-92.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_ordered | inferred
  > if self.from_ is not None and self.until is not None and self.from_ >= self.until:
