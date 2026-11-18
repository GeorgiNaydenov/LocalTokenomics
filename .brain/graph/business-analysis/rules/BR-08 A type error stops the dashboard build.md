---
code: BR-08
category: quality
tags:
  - ba/rule
maturity: approved
---
# A type error stops the dashboard build

## Statement

The web build script runs the TypeScript check before Vite, so a type error prevents a bundle from being written.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/package.json | confirmed
  > "build": "tsc --noEmit && vite build",
