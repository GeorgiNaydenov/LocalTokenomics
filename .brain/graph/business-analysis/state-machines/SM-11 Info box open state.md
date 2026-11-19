---
code: SM-11
entity: MetricInfo
tags:
  - ba/state-machine
maturity: draft
---
# Info box open state

## States

Closed, Open.

## Transitions

Closed to Open when the pointer has stayed on the trigger or the box for 400 ms `web/src/components/metric-info.tsx:92`, when the trigger gets keyboard focus `web/src/components/metric-info.tsx:134`, or on a click `web/src/components/metric-info.tsx:143`. Open to Closed when the pointer has been outside both for 250 ms and the trigger is not focused `web/src/components/metric-info.tsx:105`, on a second click, or on any close request of the popover `web/src/components/metric-info.tsx:116`.

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/components/metric-info.tsx::MetricInfo | confirmed
  >   const [open, setOpen] = useState(false)
