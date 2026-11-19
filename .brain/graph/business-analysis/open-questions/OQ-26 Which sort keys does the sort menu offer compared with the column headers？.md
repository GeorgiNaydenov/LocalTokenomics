---
code: OQ-26
priority: low
tags:
  - ba/open-question
maturity: draft
---
# Which sort keys does the sort menu offer compared with the column headers?

## Question

The column headers can sort by client, model, id and outcome, but the option list of the sort menu has no entry for them, so the menu value after a header press has no matching option. Checked web/src/prototype/SessionsScreen.tsx and web/src/prototype/data.ts; how the menu shows an unknown value is decided in the shared component.
