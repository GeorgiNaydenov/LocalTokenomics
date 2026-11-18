---
code: RSK-02
tags:
  - ba/risk
maturity: approved
---
# Design system README and migration guide are out of date

## Risk

The README says the shipped dashboard still runs on the old src/ds CSS system, but the shipped entry point already imports the new theme and the ds folder is absent.

## Mitigation

Open question for the owner of the web folder; this chunk does not edit those files.
