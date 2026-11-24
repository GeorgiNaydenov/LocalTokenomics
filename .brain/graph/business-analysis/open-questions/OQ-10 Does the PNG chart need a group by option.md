---
code: OQ-10
priority: low
tags:
  - ba/open-question
maturity: approved
---
# Does the PNG chart need a group by option

## Question

write_png always charts model, project, day and token mix and ignores the grouping the user chose in scan. Is that intended?

## Sources

- [[Code of localtokenomics]] @ src/ai_usage_cost/render/png.py:18-18 | inferred
  > def write_png(report: Report, out: Path, dpi: int = 140) -> None:
