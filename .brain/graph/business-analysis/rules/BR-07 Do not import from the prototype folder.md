---
code: BR-07
unlinked_reason: No use case cites the file this is declared in, a file it imports directly or a file that imports it.
tags:
  - ba/rule
maturity: approved
---
# Do not import from the prototype folder

## Statement

The migration guide tells porters to copy the composition of a prototype screen and never to import from the prototype folder.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/design-system/MIGRATION.md | confirmed
  > from `prototype/` — it is mock data; copy the composition, not the module.
