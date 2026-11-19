---
code: OQ-21
priority: low
tags:
  - ba/open-question
maturity: draft
---
# Should the toast host ship in the main app

## Question

In the web source only the prototype page mounts the toast host, and the shipped dashboard entry mounts only the tooltip provider. Is the toast primitive meant for a later screen or is it dead code in the shipped app? `web/src/prototype/Prototype.tsx:109` `web/src/main.tsx:9`
