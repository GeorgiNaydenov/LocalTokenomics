---
code: RSK-14
impact: low
likelihood: medium
tags:
  - ba/risk
maturity: approved
---
# Silent row truncation in terminal tables

## Risk

Only 30 rows are printed and nothing tells the user that more exist.

## Mitigation

Print a note when buckets are cut.

## Sources

- [[Code of localtokenomics]] @ declared-in -> src/ai_usage_cost/render/terminal.py::_bucket_table | inferred
  > for bucket in rows[:30]:
