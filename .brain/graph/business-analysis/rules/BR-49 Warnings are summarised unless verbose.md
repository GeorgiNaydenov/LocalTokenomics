---
code: BR-49
tags:
  - ba/rule
maturity: approved
---
# Warnings are summarised unless verbose

## Statement

Without the verbose flag the terminal shows only the number of warnings.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/terminal.py::render | confirmed
  > elif report.warnings:
