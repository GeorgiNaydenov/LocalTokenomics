---
code: BR-46
tags:
  - ba/rule
maturity: approved
---
# Terminal table shows at most 30 rows

## Statement

The terminal breakdown table prints only the first 30 buckets, with no notice that rows were cut.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/terminal.py::_bucket_table | confirmed
  > for bucket in rows[:30]:
