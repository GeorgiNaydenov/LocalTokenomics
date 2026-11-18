---
code: BR-10
category: quality
tags:
  - ba/rule
maturity: approved
---
# Lint skips build output

## Statement

ESLint ignores the local dist folder and the bundle inside the Python package.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/eslint.config.js | confirmed
  > { ignores: ['dist', '../src/ai_usage_cost/web/dist'] },
