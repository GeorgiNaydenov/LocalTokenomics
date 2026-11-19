---
code: RSK-25
impact: medium
likelihood: low
tags:
  - ba/risk
maturity: draft
---
# One broken reader module stops the registry

## Risk

The registry imports every module of the package with no guard, so an import error in a single reader raises out of the registry call and no reader can be used until the module is fixed.

## Mitigation

Catch the import error per module, skip that reader and report a warning naming it.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/sources/__init__.py | confirmed
  > module = importlib.import_module(f"{__name__}.{info.name}")
