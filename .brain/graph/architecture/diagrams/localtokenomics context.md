---
category: context
notation: c4-context
title: Who uses localtokenomics and what it touches
answers: Which people and outside services reach the application, and which systems it is built from?
format: mermaid
serves:
  systems:
    - Ai usage cost
    - Ai usage cost render
    - Ai usage cost sources
    - Web
    - Web UI components
    - Web prototype
    - Web ui UI components
    - localtokenomics root
tags:
  - arch/diagram
maturity: draft
---
# localtokenomics context

## Description

Legend: rounded boxes are people or outside services; the boxes inside Application are its systems. Drawn from the actor and system notes; it shows who reaches the application, not each call.

## Diagram

```mermaid
flowchart LR
  subgraph APP["Application"]
    S1["Ai usage cost"]
    S2["Ai usage cost render"]
    S3["Ai usage cost sources"]
    S4["Web"]
    S5["Web UI components"]
    S6["Web prototype"]
    S7["Web ui UI components"]
    S8["localtokenomics root"]
  end
  A1("AI coding tool logs")
  A1 --> APP
  A2("CLI user")
  A2 --> APP
  A3("Dashboard developer")
  A3 --> APP
  A4("Dashboard reader")
  A4 --> APP
  A5("Maintainer")
  A5 --> APP
  A6("Notification target")
  A6 --> APP
  A7("Person using the tool")
  A7 --> APP
  A8("User of Ai usage cost")
  A8 --> APP
  A9("User of Ai usage cost sources")
  A9 --> APP
  A10("User of Web prototype")
  A10 --> APP
  A11("User of localtokenomics root")
  A11 --> APP
```
