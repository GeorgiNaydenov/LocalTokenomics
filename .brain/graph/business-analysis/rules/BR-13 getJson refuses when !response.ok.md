---
code: BR-13
category: guard
tags:
  - ba/rule
maturity: approved
---
# getJson refuses when !response.ok

## Statement

In getJson, when !response.ok: the code throws ApiError, message "${path} responded ${response.status} ${response.statusText}". Located at web/src/api.ts lines 496-497.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/api.ts::getJson | inferred
  > if (!response.ok) {
