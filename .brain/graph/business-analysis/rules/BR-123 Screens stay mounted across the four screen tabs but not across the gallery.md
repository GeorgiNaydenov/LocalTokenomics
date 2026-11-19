---
code: BR-123
tags:
  - ba/rule
maturity: draft
---
# Screens stay mounted across the four screen tabs but not across the gallery

## Statement

The Screens component owns the filter state and the active session. It stays mounted while the tab moves between the four screens, and it is replaced by the gallery for the design system tab, so a visit to the gallery resets the filters.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Prototype.tsx | confirmed
  > {tab === 'gallery' ? (
- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Screens.tsx | confirmed
  > const [filters, setFilters] = useState<FilterState>(INITIAL_FILTERS)
