---
code: RSK-45
impact: medium
likelihood: low
tags:
  - ba/risk
maturity: draft
---
# Risk 5: Sessions are identified by session id alone in the table and when opened

## Risk

The sessions table keys its rows and opens the workspace by session id only, and the shell looks the row up by that id alone, so two sources that share a session id collide and the first match opens. `web/src/Sessions.tsx:354` `web/src/App.tsx:285`

## Mitigation

Pass the source with the session id, as the workspace key already does. `web/src/App.tsx:344`
