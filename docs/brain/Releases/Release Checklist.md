---
title: Release Checklist
aliases: []
tags: [generated, operations, runbook]
area: operations
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Release Checklist

The ordered release steps the repository itself shows, each with its source.

%% generated:release-steps start (do not edit; run brain docs generate) %%
| Step | What | Source |
|---|---|---|
| 1 | Raise the version | [[pyproject.toml]] `pyproject.toml:3` |
| 2 | Raise the version | [[web/package.json]] `web/package.json:4` |
| 3 | Add the release to the changelog | [[CHANGELOG.md]] `CHANGELOG.md:1` |
| 4 | Run the checks workflows before tagging: `codeql.yml`, `python.yml`, `web.yml` | `.github/workflows/codeql.yml:1` |
| 5 | Run the script `build` | [[web/package.json]] `web/package.json:8` |

A step is listed only when a file shows it. Missing steps are not guessed.
%% generated:release-steps end %%
