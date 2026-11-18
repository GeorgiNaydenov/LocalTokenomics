---
code: BR-52
tags:
  - ba/rule
maturity: approved
---
# Empty project panel is left blank

## Statement

When the report has no project buckets the project chart panel is switched off instead of drawn.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/png.py::_cost_by_project | confirmed
  > ax.set_axis_off()
