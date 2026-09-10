import * as React from 'react'
import { useEffect, useRef, useState } from 'react'

import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { cn } from '@/design-system/cn'

const CHECK_INTERVAL_MS = 100
const OPEN_AFTER_MS = 400
const CLOSE_AFTER_MS = 250

export type MetricInfoContent =
  | { kind: 'simple'; text: string }
  | {
      kind: 'metric'
      meaning: string
      formula?: string
      computed?: string
      provenance?: string
      caveats?: string
    }

function within(rect: DOMRect, x: number, y: number): boolean {
  return x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom
}

// The last real pointer position on the page, tracked once, globally, by a single listener
// shared by every MetricInfo instance -- the sole source of truth both for deciding when to
// open (hovering the trigger) and when to close (no longer hovering either element), so the
// two decisions can never disagree with each other the way a native onMouseEnter on one
// element and a separate leave-tracking mechanism on another element otherwise could.
let lastPointer = { x: -1, y: -1 }
if (typeof window !== 'undefined') {
  window.addEventListener(
    'pointermove',
    (event) => {
      lastPointer = { x: event.clientX, y: event.clientY }
    },
    { passive: true },
  )
}

export function MetricInfo({
  content,
  children,
  className,
  triggerClassName,
  triggerStyle,
  ariaLabel = 'Explain this metric',
}: {
  content: MetricInfoContent
  children: React.ReactNode
  className?: string
  triggerClassName?: string
  triggerStyle?: React.CSSProperties
  ariaLabel?: string
}) {
  const [open, setOpen] = useState(false)
  const openRef = useRef(open)
  useEffect(() => {
    openRef.current = open
  }, [open])
  const focused = useRef(false)
  const insideSince = useRef<number | null>(null)
  const outsideSince = useRef<number | null>(null)
  const triggerRef = useRef<HTMLSpanElement | null>(null)
  const contentRef = useRef<HTMLDivElement | null>(null)

  // Polls the last known pointer position on a fixed cadence, rather than reacting only to
  // enter/leave DOM events fired on two separately positioned elements (the trigger, and the
  // content, which renders in a portal Radix can reposition after it opens). Deciding both
  // open and close from the same polled position means there is exactly one definition of
  // "the pointer is over this popover" for the whole component, checked on a schedule that
  // does not depend on the pointer continuing to move once it has already left.
  useEffect(() => {
    const id = window.setInterval(() => {
      const { x, y } = lastPointer
      const overTrigger = triggerRef.current ? within(triggerRef.current.getBoundingClientRect(), x, y) : false
      const overContent = contentRef.current ? within(contentRef.current.getBoundingClientRect(), x, y) : false
      const hovering = overTrigger || overContent

      if (hovering) {
        outsideSince.current = null
        if (openRef.current) return
        if (insideSince.current === null) {
          insideSince.current = Date.now()
          return
        }
        if (Date.now() - insideSince.current >= OPEN_AFTER_MS) {
          insideSince.current = null
          setOpen(true)
        }
        return
      }

      insideSince.current = null
      if (!openRef.current || focused.current) return
      if (outsideSince.current === null) {
        outsideSince.current = Date.now()
        return
      }
      if (Date.now() - outsideSince.current >= CLOSE_AFTER_MS) {
        outsideSince.current = null
        setOpen(false)
      }
    }, CHECK_INTERVAL_MS)
    return () => window.clearInterval(id)
  }, [])

  return (
    <Popover
      open={open}
      onOpenChange={(next) => {
        if (!next) {
          focused.current = false
          outsideSince.current = null
        } else {
          insideSince.current = null
        }
        setOpen(next)
      }}
    >
      <PopoverTrigger asChild>
        <span
          ref={triggerRef}
          tabIndex={0}
          role="button"
          aria-label={ariaLabel}
          className={cn('cursor-default rounded-sm outline-offset-2', triggerClassName)}
          style={triggerStyle}
          onFocus={() => {
            focused.current = true
            setOpen(true)
          }}
          onBlur={() => {
            focused.current = false
          }}
          onClick={(event) => {
            event.stopPropagation()
            setOpen((current) => !current)
          }}
        >
          {children}
        </span>
      </PopoverTrigger>
      <PopoverContent
        ref={contentRef}
        side="right"
        align="start"
        sideOffset={14}
        collisionPadding={12}
        avoidCollisions
        // Radix returns focus to the trigger when the content closes (the right default
        // for a dialog-like popover opened by a click). Here that is actively harmful: the
        // trigger's own onFocus reopens the popover for keyboard users tabbing to it, so an
        // auto-close that hands focus back would immediately trigger its own reopen --
        // close, refocus, reopen, forever. A hover/tap-driven info box should not steal or
        // restore focus on close at all.
        onCloseAutoFocus={(event) => event.preventDefault()}
        className={cn('w-80 text-xs', className)}
      >
        {content.kind === 'simple' ? (
          <p className="leading-relaxed text-muted-foreground">{content.text}</p>
        ) : (
          <div className="space-y-2">
            <p className="leading-relaxed text-popover-foreground">{content.meaning}</p>
            {content.formula ? (
              <p className="rounded-sm bg-muted/60 px-2 py-1 font-mono text-[11px] text-muted-foreground">
                {content.formula}
              </p>
            ) : null}
            {content.computed ? (
              <p className="rounded-sm bg-muted/60 px-2 py-1 font-mono text-[11px] text-popover-foreground">
                {content.computed}
              </p>
            ) : null}
            {content.provenance ? (
              <p className="text-muted-foreground">{content.provenance}</p>
            ) : null}
            {content.caveats ? (
              <p className="text-muted-foreground italic">{content.caveats}</p>
            ) : null}
          </div>
        )}
      </PopoverContent>
    </Popover>
  )
}

export function InfoGlyph({ className }: { className?: string }) {
  return (
    <span
      aria-hidden
      className={cn(
        'inline-flex size-3.5 shrink-0 items-center justify-center rounded-full border border-current text-[9px] leading-none text-muted-foreground',
        className,
      )}
    >
      i
    </span>
  )
}
