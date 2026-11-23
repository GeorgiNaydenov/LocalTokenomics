---
code: RSK-21
impact: medium
likelihood: low
tags:
  - ba/risk
maturity: draft
---
# A mistyped settings file silently drops the project exclusions

## Risk

One wrong value in the settings file, for example text where a number belongs, makes the whole file fall back to defaults. A project named in exclude_projects is then no longer excluded at ingest, and nothing tells the user.

## Mitigation

Raise a warning when the file exists but fails to load or validate, or validate each key on its own so one bad key cannot discard the others.

## Sources

- [[Code of localtokenomics]] | confirmed
  > except ValidationError:
- [[Code of localtokenomics]] | confirmed
  > exclude_projects=config.exclude_projects,
