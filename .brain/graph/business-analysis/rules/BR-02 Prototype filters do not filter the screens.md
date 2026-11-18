---
code: BR-02
tags:
  - ba/rule
maturity: approved
---
# Prototype filters do not filter the screens

## Statement

The filter rail in the prototype changes its own state and chips, but the screens are rendered without any filter value, so the figures on screen never change.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Screens.tsx | confirmed
  > const [filters, setFilters] = useState<FilterState>(INITIAL_FILTERS)
- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Screens.tsx | confirmed
  > <SessionsScreen onOpen={setActive} />
