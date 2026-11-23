---
code: BR-35
category: design system
tags:
  - ba/rule
maturity: approved
---
# Toggle group settings win over item settings

## Statement

A toggle group passes its variant, size and spacing to its items through a context, and an item uses its own variant or size only when the group sets none.

## Enforced in

- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/ui/toggle-group.tsx::ToggleGroupItem | confirmed
  > data-variant={context.variant || variant}
