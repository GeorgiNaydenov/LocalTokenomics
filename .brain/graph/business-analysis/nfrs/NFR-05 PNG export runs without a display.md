---
code: NFR-05
target: no display server required
tags:
  - ba/nfr
maturity: approved
---
# PNG export runs without a display

## Statement

The picture writer selects the non interactive Agg backend before importing pyplot.

## Sources

- [[Code of localtokenomics]] | confirmed
  > matplotlib.use("Agg")
