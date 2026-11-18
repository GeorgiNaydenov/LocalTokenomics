---
code: UC-16
primary_actor: CLI user
tags:
  - ba/use-case
maturity: approved
---
# Export a usage and cost chart as a PNG image

## Description

A user runs the export command with a .png output path and receives a four panel chart of the report.

## Preconditions

The output file name ends in .png.

## Postconditions

An image file exists at the output path and the command prints its path.

## Main flow

1. 1. The user runs export with a path; the command builds the report and checks the file extension. `src/ai_usage_cost/cli.py:186`
2. 2. For .png it calls the picture writer. `src/ai_usage_cost/cli.py:192`
3. 3. The writer sets a title with cost, tokens and requests and draws cost per day, cost by model, token mix and cost by project. `src/ai_usage_cost/render/png.py:26`
4. 4. It creates the parent folder and saves the figure, then closes it. `src/ai_usage_cost/render/png.py:32`

## Alternative flows

Step 1 alt: an extension other than .json or .png prints an error and exits with code 2. `src/ai_usage_cost/cli.py:56`

## Acceptance criteria

The chart is written with the Agg backend, so no display is needed. `src/ai_usage_cost/render/png.py:9`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/render/png.py::write_png | confirmed
  > def write_png(
