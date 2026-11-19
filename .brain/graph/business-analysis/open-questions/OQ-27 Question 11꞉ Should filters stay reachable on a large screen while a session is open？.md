---
code: OQ-27
priority: medium
tags:
  - ba/open-question
maturity: draft
---
# Question 11: Should filters stay reachable on a large screen while a session is open?

## Question

On a large screen the filter rail is hidden while a workspace is open and the Filters button is hidden at that breakpoint, so the filters cannot be reached until the workspace closes. Is that intended? See web/src/App.tsx (docked), web/src/FilterRail.tsx (aside) and web/src/Header.tsx (Filters button).
