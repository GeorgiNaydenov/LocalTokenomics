---
code: OQ-29
priority: medium
tags:
  - ba/open-question
maturity: draft
---
# Question 13: Should failed tabs and span texts offer a retry?

## Question

A workspace tab whose endpoint failed and a span text that failed both keep the error with no retry until the session is reopened. Is a retry wanted? See web/src/SessionWorkspace.tsx (LoadableTab) and web/src/TraceTab.tsx (toggleContent).

## Sources

- [[Code of localtokenomics]] @ web/src/SessionWorkspace.tsx:433-433 | inferred
  > export default function SessionWorkspace(props: {
