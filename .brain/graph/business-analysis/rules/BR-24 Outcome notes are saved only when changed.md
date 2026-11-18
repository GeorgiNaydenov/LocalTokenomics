---
code: BR-24
tags:
  - ba/rule
maturity: approved
---
# Outcome notes are saved only when changed

## Statement

Notes and tags are sent to the server on blur only when the text differs from the saved value.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/SessionWorkspace.tsx | confirmed
  > if (current.notes === persisted.notes && current.tagsText === persisted.tagsText) return
