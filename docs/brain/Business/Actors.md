---
title: Actors
aliases: []
tags: [actors, business, generated, spec]
area: business
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/cli.py, src/ai_usage_cost/sources/base.py]
generated: true
anchors: true
---

# Actors

> [!info] What this is
> The people and systems that use the application, and the use cases each one starts or takes part in.

## AI coding tool logs

The files and databases that AI coding tools write on the machine. They are read and never changed: [[src/ai_usage_cost/sources/base.py|src/ai_usage_cost/sources/base.py:123]].

- **Kind:** external
- **Use cases:** [[UC-17 See what my AI usage would cost]]

Source:
- `Source`: `class Source:`

## CLI user

The person who runs the scan or export command in a terminal.

- **Kind:** human
- **Use cases:** [[UC-15 Print a usage and cost summary in the terminal]], [[UC-16 Export a usage and cost chart as a PNG image]]

Source:
- `scan`: `def scan(`

## Dashboard developer

A person who builds or restyles the dashboard and opens the prototype to see how a screen or component should look.

- **Kind:** human
- **Use cases:** [[UC-01 Compare a dashboard screen with its reference]]


## Dashboard reader

The person who opens the local dashboard to read usage and list price cost. The code has no login or role check, so there is one human actor.

- **Kind:** human
- **Use cases:** [[UC-05 Read usage and cost for a period]], [[UC-06 Inspect one session]], [[UC-07 Rate a session outcome]], [[UC-08 Check list prices]], [[UC-09 Read a figure and see how far to trust it]], [[UC-10 Narrow a list and choose its columns]], [[UC-11 Inspect a chart point]], [[UC-12 Review a session's spans and context use]]

Source:
- [[web/src/main.tsx|web/src/main.tsx]]: `createRoot(document.getElementById('root') as HTMLElement).render(`

## GitHub workflow runner

The hosted runner that executes the Python, web and CodeQL workflows on pull requests, pushes to main and a weekly schedule.

- **Kind:** system
- **Use cases:** [[UC-04 Check a change before merge]]

Source:
- `.github/workflows/web.yml`: `runs-on: ubuntu-latest`

## Maintainer

A person who changes the dashboard source or the Python package and runs the build and the checks.

- **Kind:** human
- **Use cases:** [[UC-02 Rebuild the dashboard bundle]], [[UC-03 Develop the dashboard against live data]]

Source:
- [[web/package.json|web/package.json]]: `"build": "tsc --noEmit && vite build",`

## Notification target

A service reached through an Apprise address the person passes to the alert command: [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:344]].

- **Kind:** external
- **Use cases:** [[UC-20 Be alerted when spend rises]]

Source:
- `alert`: `notifier = apprise.Apprise()`

## Person using the tool

The owner of the machine who runs the commands and opens the dashboard. The code has no other role and no login: [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:24]].

- **Kind:** human
- **Use cases:** [[UC-17 See what my AI usage would cost]], [[UC-18 Explore spend in the dashboard]], [[UC-19 Export a report as a file]], [[UC-20 Be alerted when spend rises]], [[UC-21 Inspect and rate one session]], [[UC-22 Forget a session]], [[UC-23 Read the text of one span]], [[UC-24 Try the tool with demo data]], [[UC-25 Sample GPU use for local models]], [[UC-26 Query the store with SQL]], [[UC-27 Browse sessions in the terminal]]

Source:
- `app`: `app = typer.Typer(`

## User of Ai usage cost

A person who calls the 12 routes or opens the 0 screens of the Ai usage cost module. The code does not name roles; the agent refines this actor when roles are visible.

- **Kind:** human

Source:
- [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py]]: `def meta() -> Meta:`

## User of localtokenomics root

A person who calls the 0 routes or opens the 1 screens of the localtokenomics root module. The code does not name roles; the agent refines this actor when roles are visible.

- **Kind:** human

Source:
- [[web/index.html|web/index.html]]: `<!doctype html>`
