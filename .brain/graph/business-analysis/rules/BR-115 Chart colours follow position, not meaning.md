---
code: BR-115
tags:
  - ba/rule
maturity: draft
---
# Chart colours follow position, not meaning

## Statement

The picture writer takes colours from one seven colour list by position. In the cost per day chart a colour is a client, in the model chart a rank, and in the token mix chart a token bucket, so the same colour means a different thing in each panel.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/png.py | confirmed
  > color=PALETTE[index % len(PALETTE)],
- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/png.py | confirmed
  > color=[PALETTE[i % len(PALETTE)] for i in range(len(buckets))],
- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/render/png.py | confirmed
  > ax.barh(labels, values, left=left, label=name, color=PALETTE[index % len(PALETTE)])
