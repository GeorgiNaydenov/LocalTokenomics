---
code: BR-01
tags:
  - ba/rule
maturity: approved
---
# The prototype is excluded from the production build

## Statement

The production build writes to the Python package folder from a single page, and the repository guide states the prototype page is deliberately left out of it.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/vite.config.ts | confirmed
  > outDir: '../src/ai_usage_cost/web/dist',
- [[Code of localtokenomics]] @ enforced-by -> web/src/design-system/MIGRATION.md | confirmed
  > inside the Python wheel. It must stay working. `prototype.html` is deliberately excluded
