---
code: OQ-24
priority: medium
tags:
  - ba/open-question
maturity: draft
---
# Is the offline card matched by message text on purpose

## Question

The app decides that the reader is offline by looking for a fixed sentence in the error text before it draws the offline card, so a reworded message would show the plain error card instead. Should the failure carry a typed marker? `web/src/App.tsx:251`
