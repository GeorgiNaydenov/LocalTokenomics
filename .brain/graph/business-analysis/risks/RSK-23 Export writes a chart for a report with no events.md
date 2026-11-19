---
code: RSK-23
tags:
  - ba/risk
maturity: draft
---
# Export writes a chart for a report with no events

## Risk

The scan command refuses an empty report with a hint and exit code 1, but the export command has no such check, so a png export of an empty report writes a figure with a zero cost title and empty axes and then prints that it wrote the file.

## Mitigation

Share the empty report check between the two commands, or print a warning before the picture is written.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/cli.py | confirmed
  > if not report.totals.events:
- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/cli.py | confirmed
  > write_png(report, out)
- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/png.py | confirmed
  > fig.suptitle(
