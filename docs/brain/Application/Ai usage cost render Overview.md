---
title: Ai usage cost render Overview
aliases: []
tags: [module, overview]
area: application
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/render/**]
verified-against: ef290ff43851
chunk: ch-localtokenomics-src-ai-usage-cost-render
approved-by: human
approved-at: '2026-11-18T19:06:20+00:00'
---

# Ai usage cost render Overview

What Ai usage cost render is made of and how it connects to the rest of the code.

## How it works

Ai usage cost render holds 3 source files and 187 lines. The most depended-on files are `src/ai_usage_cost/render/png.py`, `src/ai_usage_cost/render/terminal.py`, `src/ai_usage_cost/render/__init__.py`. It uses Ai usage cost Overview. It is used by Ai usage cost Overview.

The purpose column quotes each file's own header comment where it has one. Every file is cited by its full line range, and every public name by the line that declares it.

## What this layer does

The render layer turns a finished `Report` into something a person can read. It computes no cost itself: both files only read fields the report already holds. `src/ai_usage_cost/render/terminal.py:17-31` `src/ai_usage_cost/render/png.py:18-29`

There are two outputs. The terminal renderer prints text through a rich console. The picture writer saves a four panel chart as an image file. `src/ai_usage_cost/render/terminal.py:17-20` `src/ai_usage_cost/render/png.py:18-19`

The package file `src/ai_usage_cost/render/__init__.py` is empty, so a caller imports the two modules directly. `src/ai_usage_cost/cli.py:22-22` `src/ai_usage_cost/cli.py:190-190`

## Terminal output

The renderer first prints a Total panel. It shows the API-equivalent cost, the token and request counts, the number of sessions, the date span of the data, the number of log files scanned and the date of the rates. When no event has a time, the span reads "no data". `src/ai_usage_cost/render/terminal.py:49-61`

A second line about prompt caching appears only when the saving is above zero. It states the saving and what the cost would have been without caching. `src/ai_usage_cost/render/terminal.py:62-66`

One breakdown table follows. The caller picks the grouping by model, client, provider, project or day, and an unknown name falls back to model. The table is skipped when the chosen list is empty. `src/ai_usage_cost/render/terminal.py:22-31`

Each table has the cost, four token columns (input, cache read, cache write, output) and the request count. It prints at most 30 rows and says nothing about rows it left out. The day grouping is sorted oldest first and the others keep the order the report gave them. `src/ai_usage_cost/render/terminal.py:70-85`

Models without a rate are shown in their own table, described as excluded from totals, with a reminder to add them to rates.json. `src/ai_usage_cost/render/terminal.py:33-40`

Warnings are printed in full only when the verbose flag is set. Otherwise the renderer prints how many there are and how to see them. `src/ai_usage_cost/render/terminal.py:42-46`

## Image output

The picture writer makes a two by two figure. Its title carries the cost, the token count and the request count. The panels are cost per day stacked by client, cost by model, token mix by model, and cost by project. `src/ai_usage_cost/render/png.py:19-29`

It selects the Agg backend before importing pyplot, so it works without a display. `src/ai_usage_cost/render/png.py:7-11`

The model cost chart shows the top 10 models, the token mix chart the top 8, and the project chart the top 10. The project panel is turned off when the report has no project buckets. `src/ai_usage_cost/render/png.py:59-59` `src/ai_usage_cost/render/png.py:71-71` `src/ai_usage_cost/render/png.py:90-93`

A seven color palette is reused by position and wraps around when there are more items. `src/ai_usage_cost/render/png.py:15-15` `src/ai_usage_cost/render/png.py:49-49`

The writer creates the missing parent folders of the output path, saves the figure at the given resolution (140 dots per inch by default) and closes it. `src/ai_usage_cost/render/png.py:18-18` `src/ai_usage_cost/render/png.py:31-33`

## Who calls it

Only the command line calls these functions. The scan command renders to the terminal after building the report, and exits with code 1 and a hint when no usage was found. The export command calls the picture writer for a .png path and refuses extensions other than .json and .png. `src/ai_usage_cost/cli.py:98-105` `src/ai_usage_cost/cli.py:186-195`

## What to know

The dashboard does not read anything from this layer. The report it shows is served by the HTTP route in `src/ai_usage_cost/api.py:289-289`, and the same report can be printed as JSON by the scan command. `src/ai_usage_cost/cli.py:95-97`

The picture writer ignores the grouping option of the scan command, because export takes no such option. `src/ai_usage_cost/cli.py:176-183`

No test file in the repository imports this folder, so the output format has no test of its own here.

The components are drawn in [[Render layer components]].

## Reference

%% generated:chunk-files start (do not edit; run brain docs generate) %%
### Files

| File | Purpose | Lines | Imports | Imported by | Code |
|---|---|---|---|---|---|
| `src/ai_usage_cost/render/__init__.py` | - | 0 | 0 | 0 | empty file |
| `src/ai_usage_cost/render/png.py` | - | 101 | 1 | 1 | [[src/ai_usage_cost/render/png.py]] `src/ai_usage_cost/render/png.py:1-101` |
| `src/ai_usage_cost/render/terminal.py` | - | 86 | 1 | 1 | [[src/ai_usage_cost/render/terminal.py]] `src/ai_usage_cost/render/terminal.py:1-86` |
%% generated:chunk-files end %%

%% generated:chunk-interface start (do not edit; run brain docs generate) %%
### Public interface

| Name | Kind | File | Code |
|---|---|---|---|
| `write_png` | function | `src/ai_usage_cost/render/png.py` | [[src/ai_usage_cost/render/png.py]] `src/ai_usage_cost/render/png.py:18` |
| `render` | function | `src/ai_usage_cost/render/terminal.py` | [[src/ai_usage_cost/render/terminal.py]] `src/ai_usage_cost/render/terminal.py:17` |
%% generated:chunk-interface end %%
