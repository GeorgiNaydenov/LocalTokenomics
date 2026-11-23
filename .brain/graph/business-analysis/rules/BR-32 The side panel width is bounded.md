---
code: BR-32
category: validation
tags:
  - ba/rule
maturity: approved
---
# The side panel width is bounded

## Statement

The workspace side panel is at least 360 pixels wide and at most 900 pixels or 90 percent of the window, whichever is smaller.

## Enforced in

- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/workspace-panel.ts::clampWidth | confirmed
  >   return Math.min(bound, Math.max(MIN_WIDTH, width))
