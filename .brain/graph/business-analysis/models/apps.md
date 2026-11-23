---
archetype: entity
fields:
  - 'id: INTEGER (PK, required)'
  - 'name: TEXT'
  - 'path: TEXT'
  - 'created_at: INTEGER'
  - 'updated_at: INTEGER'
  - 'github_org: TEXT'
  - 'github_repo: TEXT'
  - 'chat_context: TEXT'
  - 'github_branch: TEXT'
  - 'vercel_project_id: TEXT'
  - 'vercel_project_name: TEXT'
  - 'vercel_team_id: TEXT'
  - 'vercel_deployment_url: TEXT'
  - 'neon_project_id: TEXT'
  - 'neon_development_branch_id: TEXT'
  - 'neon_preview_branch_id: TEXT'
entity_keys:
  - id
relations_to: []
tags:
  - ba/model
maturity: approved
---
# apps

## Description

The table apps apps, declared in src/ai_usage_cost/demo.py lines 52-69. It has 16 fields and 0 relations.

## Attributes

- id: INTEGER (PK, required)
- name: TEXT
- path: TEXT
- created_at: INTEGER
- updated_at: INTEGER
- github_org: TEXT
- github_repo: TEXT
- chat_context: TEXT
- github_branch: TEXT
- vercel_project_id: TEXT
- vercel_project_name: TEXT
- vercel_team_id: TEXT
- vercel_deployment_url: TEXT
- neon_project_id: TEXT
- neon_development_branch_id: TEXT
- neon_preview_branch_id: TEXT

## Lifecycle

No lifecycle field was found in the code.

## Used by

- [[UC-13 Discover AI tool usage from local files]]
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

- [[Code of localtokenomics]] @ manifests-as -> src/ai_usage_cost/demo.py::apps | inferred
  > CREATE TABLE apps (
