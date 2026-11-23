---
code: RSK-26
impact: low
likelihood: low
tags:
  - ba/risk
maturity: draft
---
# Two readers import a private name from the Cline module

## Risk

Roo Code and Kilo Code legacy import _TOKENS_IN_INCLUSIVE, a name that starts with an underscore, from the Cline module, so a rename inside Cline breaks them without a public contract saying so.

## Mitigation

Expose the table under a public name or pass the flag through Spec.

## Sources

- [[Code of localtokenomics]] | confirmed
  > from .cline import _TOKENS_IN_INCLUSIVE, Spec, make_source, task_roots
- [[Code of localtokenomics]] | confirmed
  > from .cline import _TOKENS_IN_INCLUSIVE, Spec, make_source, task_roots
