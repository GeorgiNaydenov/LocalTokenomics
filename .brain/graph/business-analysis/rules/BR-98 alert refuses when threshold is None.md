---
code: BR-98
category: guard
tags:
  - ba/rule
maturity: approved
---
# alert refuses when threshold is None

## Statement

In alert, when threshold is None: the code raises typer.BadParameter, message "pass --over (window total) or --rise-over (rise vs before)". Located at src/ai_usage_cost/cli.py lines 325-326.

## Enforced in

- [[UC-15 Print a usage and cost summary in the terminal]]
- [[UC-16 Export a usage and cost chart as a PNG image]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-19 Export a report as a file]]
- [[UC-20 Be alerted when spend rises]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]
- [[UC-24 Try the tool with demo data]]
- [[UC-25 Sample GPU use for local models]]
- [[UC-26 Query the store with SQL]]
- [[UC-27 Browse sessions in the terminal]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/cli.py::alert | inferred
  > if threshold is None:
