---
code: BR-51
tags:
  - ba/rule
maturity: approved
---
# PNG charts are limited to the top buckets

## Statement

The model cost chart and project cost chart show at most 10 buckets and the token mix chart at most 8 models.

## Enforced in

- [[UC-15 Print a usage and cost summary in the terminal]]
- [[UC-16 Export a usage and cost chart as a PNG image]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-19 Export a report as a file]]
- [[UC-20 Be alerted when spend rises]]
- [[UC-24 Try the tool with demo data]]
- [[UC-25 Sample GPU use for local models]]
- [[UC-26 Query the store with SQL]]
- [[UC-27 Browse sessions in the terminal]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/png.py::_cost_by_model | confirmed
  > buckets = report.by_model[:10][::-1]
- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/png.py::_token_mix | confirmed
  > buckets = report.by_model[:8][::-1]
