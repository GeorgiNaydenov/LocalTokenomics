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

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/pricing.py::_ordered | inferred
  > if self.from_ is not None and self.until is not None and self.from_ >= self.until:
