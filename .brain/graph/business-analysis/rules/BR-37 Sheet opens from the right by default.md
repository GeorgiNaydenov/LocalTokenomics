---
code: BR-37
category: design system
tags:
  - ba/rule
maturity: approved
---
# Sheet opens from the right by default

## Statement

A sheet slides in from the right unless a side of top, bottom or left is given, and both sheet and dialog show a close button unless showCloseButton is false.

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/ui/sheet.tsx::SheetContent | confirmed
  > side = "right",
- [[Code of localtokenomics]] @ enforced-by -> web/src/components/ui/dialog.tsx::DialogContent | confirmed
  > showCloseButton = true,
