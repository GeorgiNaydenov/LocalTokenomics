---
code: RSK-40
tags:
  - ba/risk
maturity: draft
---
# Sessions footer asks the user to narrow filters that do nothing

## Risk

The footer note says to narrow the filters to see the rest of the sessions, but the screen receives no filter value, so the advice cannot work. A port that copies the text would promise a control the data layer does not apply.

## Mitigation

Pass the filter state into the screen when porting, or drop the sentence from the reference.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/SessionsScreen.tsx | confirmed
  > Narrow the filters to see the rest.
