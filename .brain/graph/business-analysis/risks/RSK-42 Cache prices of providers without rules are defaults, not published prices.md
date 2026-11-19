---
code: RSK-42
tags:
  - ba/risk
maturity: draft
---
# Cache prices of providers without rules are defaults, not published prices

## Risk

The pricing screen derives cache prices from the provider rules and falls back to 0.1 for reads and 1.25 for writes when the provider has none. The rule table lists three providers while the rate table also has deepseek, moonshot and mistral rows, so their cache columns show the default. The note beside the multipliers says discounts differ by provider.

## Mitigation

Show a dash, or mark the figure as a default, for providers without a rule.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/PricingScreen.tsx | confirmed
  > const rules = PROVIDER_RULES[rate.provider]
- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/data.ts | confirmed
  > export const PROVIDER_RULES: Record<string, ProviderRules> = {
