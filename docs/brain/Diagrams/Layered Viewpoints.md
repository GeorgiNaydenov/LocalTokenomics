---
title: Layered Viewpoints
aliases: []
tags: [c4, capability, diagram, mermaid]
area: diagrams
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: []
sources: [docs/brain/architecture/diagrams/application-communication.mmd, docs/brain/architecture/diagrams/technology-landscape.mmd]
---

# Layered Viewpoints

Two layered views derived from the code: how components communicate, and the technology each layer rests on.

## Application communication

%% generated:diagram-application-communication start (do not edit; run brain docs generate) %%
```mermaid
flowchart LR
    localtokenomics_root["(root)<br/>2 files<br/>0 routes"]:::system
    localtokenomics_src_ai_usage_cost["src/ai_usage_cost<br/>13 files<br/>12 routes"]:::system
    localtokenomics_src_ai_usage_cost_render["src/ai_usage_cost/render<br/>3 files<br/>0 routes"]:::system
    localtokenomics_src_ai_usage_cost_sources["src/ai_usage_cost/sources<br/>22 files<br/>0 routes"]:::system
    localtokenomics_root["(root)<br/>2 files<br/>0 routes"]:::system
    localtokenomics_web_src["web/src<br/>20 files<br/>0 routes"]:::system
    localtokenomics_web_src_components["web/src/components<br/>18 files<br/>0 routes"]:::system
    localtokenomics_web_src_components_ui["web/src/components/ui<br/>25 files<br/>0 routes"]:::system
    localtokenomics_web_src_prototype["web/src/prototype<br/>10 files<br/>0 routes"]:::system
    db_localtokenomics_src_ai_usage_cost[("Data of src-ai-usage-cost<br/>51 entities")]:::store
    localtokenomics_src_ai_usage_cost --> db_localtokenomics_src_ai_usage_cost
    db_localtokenomics_src_ai_usage_cost_sources[("Data of src-ai-usage-cost-sources<br/>2 entities")]:::store
    localtokenomics_src_ai_usage_cost_sources --> db_localtokenomics_src_ai_usage_cost_sources
    localtokenomics_root --> localtokenomics_src_ai_usage_cost
    localtokenomics_src_ai_usage_cost --> localtokenomics_src_ai_usage_cost_sources
    localtokenomics_src_ai_usage_cost --> localtokenomics_src_ai_usage_cost_render
    localtokenomics_src_ai_usage_cost_render --> localtokenomics_src_ai_usage_cost
    localtokenomics_src_ai_usage_cost_sources --> localtokenomics_src_ai_usage_cost
    localtokenomics_web_src --> localtokenomics_web_src_components
    localtokenomics_web_src --> localtokenomics_web_src_components_ui
    localtokenomics_web_src_components --> localtokenomics_web_src
    localtokenomics_web_src_components --> localtokenomics_web_src_components_ui
    localtokenomics_web_src_components_ui --> localtokenomics_web_src
    localtokenomics_web_src_prototype --> localtokenomics_web_src_components
    localtokenomics_web_src_prototype --> localtokenomics_web_src_components_ui
    localtokenomics_web_src_prototype --> localtokenomics_web_src
    subgraph Legend
        direction LR
        zlegend_a["Component: part of this system"]:::system
        zlegend_b["Data store"]:::store
        zlegend_c["System you do not control"]:::external
        zlegend_d["Solid arrow: imports or calls; dashed: call to another repository"]:::system
        zlegend_a ~~~ zlegend_b ~~~ zlegend_c ~~~ zlegend_d
    end
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
    classDef store fill:#d5e8d4,stroke:#82b366,color:#142233
    classDef external fill:#f5f5f5,stroke:#666666,color:#142233
    classDef admin fill:#ffe6cc,stroke:#d79b00,color:#142233
    classDef security fill:#e1d5e7,stroke:#9673a6,color:#142233
```
%% generated:diagram-application-communication end %%

## Technology landscape

%% generated:diagram-technology-landscape start (do not edit; run brain docs generate) %%
```mermaid
flowchart TB
    subgraph g_Languages["Languages"]
        lang_python["python"]:::system
        lang_sql["sql"]:::system
        lang_typescript["typescript"]:::system
    end
    subgraph g_Frameworks_and_libraries["Frameworks and libraries"]
        dep_pydantic["pydantic"]:::system
        dep_fastapi["fastapi"]:::system
        dep_react["react"]:::system
        dep_tailwindcss["tailwindcss"]:::system
    end
    subgraph g_Data["Data"]
        data_store["Database (from entity definitions)"]:::store
    end
    subgraph g_Build_and_delivery["Build and delivery"]
        ops__github_workflows_codeql_yml[".github/workflows/codeql.yml"]:::system
        ops__github_workflows_python_yml[".github/workflows/python.yml"]:::system
        ops__github_workflows_web_yml[".github/workflows/web.yml"]:::system
    end
    subgraph g_Tests["Tests"]
        dep_pytest["pytest"]:::system
        dep_vitest["vitest"]:::system
    end
    g_Languages --> g_Frameworks_and_libraries
    g_Frameworks_and_libraries --> g_Data
    g_Data --> g_Build_and_delivery
    g_Build_and_delivery --> g_Tests
    subgraph Legend
        direction LR
        zlegend_a["Component: part of this system"]:::system
        zlegend_d["Arrow: the layer above is implemented with the layer below"]:::system
        zlegend_a ~~~ zlegend_b ~~~ zlegend_c ~~~ zlegend_d
    end
    classDef system fill:#dae8fc,stroke:#6c8ebf,color:#142233
    classDef store fill:#d5e8d4,stroke:#82b366,color:#142233
    classDef external fill:#f5f5f5,stroke:#666666,color:#142233
    classDef admin fill:#ffe6cc,stroke:#d79b00,color:#142233
    classDef security fill:#e1d5e7,stroke:#9673a6,color:#142233
```
%% generated:diagram-technology-landscape end %%
