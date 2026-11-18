---
code: BR-51
tags:
  - ba/rule
maturity: approved
---
# PNG charts are limited to the top buckets

## Statement

The model cost chart and project cost chart show at most 10 buckets and the token mix chart at most 8 models.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/png.py::_cost_by_model | confirmed
  > buckets = report.by_model[:10][::-1]
- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/png.py::_token_mix | confirmed
  > buckets = report.by_model[:8][::-1]
