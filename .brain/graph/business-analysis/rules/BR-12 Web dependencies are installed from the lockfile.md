---
code: BR-12
category: build
tags:
  - ba/rule
maturity: approved
---
# Web dependencies are installed from the lockfile

## Statement

The web workflow installs with npm ci, which installs exactly what package-lock.json records.

## Enforced in

- [[UC-04 Check a change before merge]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> .github/workflows/web.yml | confirmed
  > run: npm ci
