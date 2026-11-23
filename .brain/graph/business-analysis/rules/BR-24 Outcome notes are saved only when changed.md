---
code: BR-24
tags:
  - ba/rule
maturity: approved
---
# Outcome notes are saved only when changed

## Statement

Notes and tags are sent to the server on blur only when the text differs from the saved value.

## Enforced in

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/SessionWorkspace.tsx | confirmed
  > if (current.notes === persisted.notes && current.tagsText === persisted.tagsText) return
