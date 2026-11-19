---
code: OQ-28
priority: low
tags:
  - ba/open-question
maturity: draft
---
# Question 12: Which warnings should the Flagged figure count?

## Question

The Flagged figure of the overview counts the warning summary of the last scan, while the Sources view lists the warning groups of the current report. Should both use the same set? See web/src/Overview.tsx (FlaggedStat) and web/src/Sources.tsx (Scan warnings panel).
