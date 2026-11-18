---
code: BR-09
category: build
tags:
  - ba/rule
maturity: approved
---
# A production build replaces the committed bundle

## Statement

Every production build empties the output folder inside the Python package before writing the new bundle.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/vite.config.ts | confirmed
  > emptyOutDir: true,
