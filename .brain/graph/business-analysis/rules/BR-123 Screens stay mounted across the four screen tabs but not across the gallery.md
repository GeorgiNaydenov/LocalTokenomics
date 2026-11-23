---
code: BR-123
tags:
  - ba/rule
maturity: draft
---
# Screens stay mounted across the four screen tabs but not across the gallery

## Statement

The Screens component owns the filter state and the active session. It stays mounted while the tab moves between the four screens, and it is replaced by the gallery for the design system tab, so a visit to the gallery resets the filters.

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-10 Narrow a list and choose its columns]]
- [[UC-12 Review a session's spans and context use]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Prototype.tsx | confirmed
  > {tab === 'gallery' ? (
- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Screens.tsx | confirmed
  > const [filters, setFilters] = useState<FilterState>(INITIAL_FILTERS)
