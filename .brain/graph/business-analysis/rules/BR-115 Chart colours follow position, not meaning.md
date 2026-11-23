---
code: BR-115
tags:
  - ba/rule
maturity: draft
---
# Chart colours follow position, not meaning

## Statement

The picture writer takes colours from one seven colour list by position. In the cost per day chart a colour is a client, in the model chart a rank, and in the token mix chart a token bucket, so the same colour means a different thing in each panel.

## Enforced in

- [[UC-15 Print a usage and cost summary in the terminal]]
- [[UC-16 Export a usage and cost chart as a PNG image]]
- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-19 Export a report as a file]]
- [[UC-20 Be alerted when spend rises]]
- [[UC-24 Try the tool with demo data]]
- [[UC-25 Sample GPU use for local models]]
- [[UC-26 Query the store with SQL]]
- [[UC-27 Browse sessions in the terminal]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/png.py | confirmed
  > color=PALETTE[index % len(PALETTE)],
- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/png.py | confirmed
  > color=[PALETTE[i % len(PALETTE)] for i in range(len(buckets))],
- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/png.py | confirmed
  > ax.barh(labels, values, left=left, label=name, color=PALETTE[index % len(PALETTE)])
