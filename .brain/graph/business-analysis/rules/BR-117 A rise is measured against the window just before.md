---
code: BR-117
category: calculation
subdomain: Spend reporting
tags:
  - ba/rule
maturity: draft
---
# A rise is measured against the window just before

## Statement

With the rise threshold the earlier window has the same length and ends the day before the current window starts. `src/ai_usage_cost/cli.py:336`

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
  > analysis, since=since - timedelta(days=days), until=since - timedelta(days=1)
