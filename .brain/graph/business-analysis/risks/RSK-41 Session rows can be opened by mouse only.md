---
code: RSK-41
tags:
  - ba/risk
maturity: draft
---
# Session rows can be opened by mouse only

## Risk

The table row has a click handler and a pointer cursor but no key handler and no tab stop, so a keyboard user cannot open a session. Only the error count has a tab stop. A screen meant as the reference for the real one should not carry this gap.

## Mitigation

Make the row focusable and open it on Enter, or put a button in the id cell, in the shipped screen.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/SessionsScreen.tsx | confirmed
  > className="cursor-pointer"
