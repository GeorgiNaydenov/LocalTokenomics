---
code: BR-10
category: quality
unlinked_reason: No use case cites the file this is declared in, a file it imports directly or a file that imports it.
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
