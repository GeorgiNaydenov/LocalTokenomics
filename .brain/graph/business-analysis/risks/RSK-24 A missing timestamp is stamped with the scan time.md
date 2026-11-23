---
code: RSK-24
impact: low
likelihood: low
tags:
  - ba/risk
maturity: draft
---
# A missing timestamp is stamped with the scan time

## Risk

Copilot Chat, Dyad and Ollama call parse_timestamp without a fallback file. When the stored time is missing or unreadable the helper returns the current time, so the event lands on the day of the scan and moves each time the file is rebuilt.

## Mitigation

Pass the file path as the fallback, as the other readers do, or skip the row and add a warning.

## Sources

- [[Code of localtokenomics]] | confirmed
  > return datetime.now(tz=UTC)
- [[Code of localtokenomics]] | confirmed
  > timestamp=parse_timestamp(timestamp),
- [[Code of localtokenomics]] | confirmed
  > timestamp=parse_timestamp(created_at),
- [[Code of localtokenomics]] | confirmed
  > timestamp=parse_timestamp(created_at),
