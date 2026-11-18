---
code: BR-30
category: display
tags:
  - ba/rule
maturity: approved
---
# A table always keeps at least one column

## Statement

If the reader hides every column, all columns are shown again.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/columns.tsx::visibleColumns | confirmed
  >   return shown.length > 0 ? shown : columns
