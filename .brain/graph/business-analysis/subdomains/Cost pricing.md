---
type: core
tags:
  - ba/subdomain
maturity: draft
---
# Cost pricing

## Description

Turns token counts into the cost the same usage would have had at published API list prices, using a rate table with periods, bands, tiers and peak windows. Main code: `src/ai_usage_cost/pricing.py:495` and `src/ai_usage_cost/pricing.py:252`.

## Sources

- [[Code of localtokenomics]] @ bounded-by -> src/ai_usage_cost/pricing.py::cost_of | inferred
  > def cost_of(
