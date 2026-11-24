---
code: OQ-25
priority: low
tags:
  - ba/open-question
maturity: draft
---
# Does the shared token cell clamp a negative bar fraction?

## Question

A session without token counts has a token total of minus one, and the table divides it by the largest total to get the bar fraction, which is then negative. The prototype does not clamp it. Checked web/src/prototype/SessionsScreen.tsx; the answer is in the shared session component, which belongs to another chunk.

## Sources

- [[Code of localtokenomics]] @ web/src/prototype/SessionsScreen.tsx:82-82 | inferred
  > export function SessionsScreen({ onOpen }: { onOpen: (session: PrototypeSession) => void }) {
