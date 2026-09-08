import * as React from 'react'
import { useCallback, useId, useRef, useState } from 'react'

import { cn } from '@/design-system/cn'

export interface HoverEntry {
  label: string
  value: string
  color?: string
}

export interface HoverDetail {
  title: string
  entries: HoverEntry[]
  note?: string
}

export function HoverFrame({
  count,
  label,
  describe,
  positionAt,
  children,
  className,
}: {
  count: number
  label: string
  describe: (index: number) => HoverDetail
  positionAt: (index: number) => number
  children: (index: number | null) => React.ReactNode
  className?: string
}) {
  const [index, setIndex] = useState<number | null>(null)
  const frame = useRef<HTMLDivElement | null>(null)
  const liveId = useId()

  const fromPointer = useCallback(
    (clientX: number) => {
      const node = frame.current
      if (!node || count === 0) return
      const rect = node.getBoundingClientRect()
      const ratio = (clientX - rect.left) / rect.width
      setIndex(Math.min(count - 1, Math.max(0, Math.floor(ratio * count))))
    },
    [count],
  )

  const step = useCallback(
    (delta: number) => {
      setIndex((current) => {
        const next = current === null ? 0 : current + delta
        return Math.min(count - 1, Math.max(0, next))
      })
    },
    [count],
  )

  const onKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'ArrowRight') step(1)
    else if (event.key === 'ArrowLeft') step(-1)
    else if (event.key === 'Home') setIndex(0)
    else if (event.key === 'End') setIndex(count - 1)
    else if (event.key === 'Escape') setIndex(null)
    else return
    event.preventDefault()
  }

  const detail = index === null ? null : describe(index)
  const anchor = index === null ? 0 : Math.min(0.98, Math.max(0.02, positionAt(index)))

  return (
    <div
      ref={frame}
      tabIndex={0}
      role="img"
      aria-label={`${label}. ${count} points. Use arrow keys to inspect.`}
      aria-describedby={liveId}
      onPointerMove={(event) => fromPointer(event.clientX)}
      onPointerLeave={() => setIndex(null)}
      onFocus={() => setIndex((current) => (current === null ? 0 : current))}
      onBlur={() => setIndex(null)}
      onKeyDown={onKeyDown}
      className={cn('relative rounded-sm outline-offset-4', className)}
    >
      {children(index)}

      {detail ? (
        <div
          aria-hidden
          className="pointer-events-none absolute bottom-full z-20 mb-2 w-max max-w-64 -translate-x-1/2 rounded-md border bg-popover px-2.5 py-2 text-popover-foreground shadow-sm"
          style={{ left: `${anchor * 100}%` }}
        >
          <p className="tabular text-[11px] font-medium">{detail.title}</p>
          <ul className="mt-1 space-y-0.5">
            {detail.entries.map((entry) => (
              <li key={entry.label} className="flex items-center gap-2 text-[11px]">
                {entry.color ? (
                  <span
                    className="size-1.5 shrink-0 rounded-full"
                    style={{ background: entry.color }}
                  />
                ) : null}
                <span className="text-muted-foreground">{entry.label}</span>
                <span className="tabular ml-auto font-medium">{entry.value}</span>
              </li>
            ))}
          </ul>
          {detail.note ? (
            <p className="mt-1.5 text-[10px] leading-snug text-muted-foreground">{detail.note}</p>
          ) : null}
        </div>
      ) : null}

      <span id={liveId} aria-live="polite" className="sr-only">
        {detail
          ? `${detail.title}. ${detail.entries.map((e) => `${e.label} ${e.value}`).join('. ')}`
          : ''}
      </span>
    </div>
  )
}
