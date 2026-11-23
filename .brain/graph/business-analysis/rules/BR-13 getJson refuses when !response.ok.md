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

## Enforced in

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-12 Review a session's spans and context use]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/api.ts::getJson | inferred
  > if (!response.ok) {
