---
classification: human
tags:
  - ba/actor
maturity: draft
---
# Person using the tool

## Description

The owner of the machine who runs the commands and opens the dashboard. The code has no other role and no login: `src/ai_usage_cost/cli.py:24`.

## Participates in

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

- [[Code of localtokenomics]] | inferred
  > app = typer.Typer(
