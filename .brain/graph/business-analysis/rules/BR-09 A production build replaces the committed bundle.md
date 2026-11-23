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

## Enforced in

- [[UC-02 Rebuild the dashboard bundle]]
- [[UC-03 Develop the dashboard against live data]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/vite.config.ts | confirmed
  > emptyOutDir: true,
