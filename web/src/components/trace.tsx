import type { KeyboardEvent, ReactNode } from 'react'
import { useRef, useState } from 'react'

import type { Capabilities, Provenance, SpanKind, SpanStatus } from '@/api'
import { HoverFrame } from '@/components/chart-hover'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import { cn } from '@/design-system/cn'
import { ProvenanceBadge } from '@/components/status'
import { StatLabel } from '@/components/stat'

export const SPAN_KIND_GLYPH: Record<SpanKind, string> = {
  turn: '¶',
  user: '»',
  assistant: '«',
  reasoning: '~',
  model_call: '◆',
  tool_call: '▶',
  tool_result: '◀',
  retrieval: '◎',
  compaction: '⇥',
  error: '✕',
  subagent: '↳',
}

export const SPAN_STATUS_COLOR: Record<SpanStatus, string> = {
  ok: 'var(--success)',
  error: 'var(--destructive)',
  interrupted: 'var(--warning)',
  aborted: 'var(--chart-8)',
  running: 'var(--primary)',
  unknown: 'var(--muted-foreground)',
}

export const HIGH_OCCUPANCY = 0.85

export interface OccupancyPoint {
  spanId: string
  startedAt: string
  occupancy: number | null
  inputTotal: number | null
  capacity: number | null
  compactedBefore: boolean
}

export function ContextOccupancy({
  points,
  height = 96,
  formatPercent,
  formatTokens,
  formatClock,
  className,
}: {
  points: OccupancyPoint[]
  height?: number
  formatPercent: (value: number) => string
  formatTokens: (value: number) => string
  formatClock: (iso: string) => string
  className?: string
}) {
  if (points.length === 0) return null

  const width = 100
  const step = width / points.length
  const barWidth = Math.max(0.6, step * 0.78)
  const known = points
    .map((point) => point.occupancy)
    .filter((value): value is number => value !== null)
  const peak = known.length ? Math.max(...known) : null
  const mean = known.length ? known.reduce((a, b) => a + b, 0) / known.length : null
  const unknown = points.length - known.length
  const y = (fraction: number) => height - Math.min(fraction, 1) * height

  return (
    <div className={cn('space-y-2', className)}>
      <HoverFrame
        count={points.length}
        label="Context window occupancy per model call"
        positionAt={(index) => (index + 0.5) / points.length}
        describe={(index) => {
          const point = points[index]
          const entries =
            point.occupancy === null
              ? [{ label: 'Occupancy', value: 'unavailable' }]
              : [
                  {
                    label: 'Occupancy',
                    value: formatPercent(point.occupancy),
                    color:
                      point.occupancy >= HIGH_OCCUPANCY ? 'var(--warning)' : 'var(--primary)',
                  },
                  ...(point.inputTotal !== null && point.capacity !== null
                    ? [
                        {
                          label: 'Input',
                          value: `${formatTokens(point.inputTotal)} of ${formatTokens(point.capacity)}`,
                        },
                      ]
                    : []),
                ]
          return {
            title: `Call ${index + 1} at ${formatClock(point.startedAt)}`,
            entries,
            note: point.compactedBefore
              ? 'Context was compacted before this call.'
              : point.occupancy === null
                ? 'This client logged no capacity, so occupancy is unknown rather than assumed.'
                : undefined,
          }
        }}
      >
        {(hovered) => (
          <svg
            viewBox={`0 0 ${width} ${height}`}
            width="100%"
            height={height}
            preserveAspectRatio="none"
            aria-hidden
            className="block"
          >
            <defs>
              <pattern
                id="occupancy-unknown"
                width={4}
                height={4}
                patternUnits="userSpaceOnUse"
                patternTransform="rotate(45)"
              >
                <rect width={4} height={4} fill="var(--muted)" />
                <line x1={0} y1={0} x2={0} y2={4} stroke="var(--border)" strokeWidth={2} />
              </pattern>
            </defs>
            <rect x={0} y={0} width={width} height={height} fill="var(--muted)" opacity={0.5} />
            {points.map((point, index) => {
              const x = index * step + (step - barWidth) / 2
              const active = hovered === index
              if (point.occupancy === null) {
                return (
                  <rect
                    key={point.spanId}
                    x={x}
                    y={0}
                    width={barWidth}
                    height={height}
                    fill="url(#occupancy-unknown)"
                    opacity={hovered === null || active ? 0.7 : 0.4}
                  />
                )
              }
              const top = y(point.occupancy)
              return (
                <g key={point.spanId}>
                  <rect
                    x={x}
                    y={top}
                    width={barWidth}
                    height={Math.max(0.8, height - top)}
                    fill={point.occupancy >= HIGH_OCCUPANCY ? 'var(--warning)' : 'var(--primary)'}
                    opacity={hovered === null || active ? 1 : 0.5}
                  />
                  {point.compactedBefore ? (
                    <rect x={x} y={0} width={barWidth} height={2} fill="var(--chart-5)" />
                  ) : null}
                </g>
              )
            })}
            {mean !== null ? (
              <line
                x1={0}
                x2={width}
                y1={y(mean)}
                y2={y(mean)}
                stroke="var(--foreground)"
                strokeOpacity={0.5}
                strokeWidth={0.6}
                strokeDasharray="2 2"
                vectorEffect="non-scaling-stroke"
              />
            ) : null}
            {peak !== null ? (
              <line
                x1={0}
                x2={width}
                y1={y(peak)}
                y2={y(peak)}
                stroke="var(--primary)"
                strokeWidth={0.6}
                strokeDasharray="3 2"
                vectorEffect="non-scaling-stroke"
              />
            ) : null}
          </svg>
        )}
      </HoverFrame>

      <div className="flex flex-wrap justify-between gap-x-4 gap-y-1 text-[11px] text-muted-foreground">
        <span className="tabular">
          {mean === null ? 'occupancy unavailable' : `mean ${formatPercent(mean)}`}
        </span>
        <span className="tabular">
          {peak === null ? `${points.length} calls` : `peak ${formatPercent(peak)}`}
        </span>
      </div>
      {unknown > 0 ? (
        <p className="text-[11px] leading-relaxed text-muted-foreground">
          {unknown === 1
            ? 'The hatched full-height bar is a call whose occupancy could not be worked out, not a call at zero.'
            : `The ${unknown} hatched full-height bars are calls whose occupancy could not be worked out, not calls at zero.`}
        </p>
      ) : null}
    </div>
  )
}

export interface TraceSpanRow {
  spanId: string
  kind: SpanKind
  name: string
  status: SpanStatus
  depth: number
  duration: ReactNode
  tokens: ReactNode
  clock?: string
  trailing?: ReactNode
  content?: ReactNode
}

export function SpanTimeline({
  spans,
  rowId,
  focusedSpanId,
  onSelectSpan,
  className,
}: {
  spans: TraceSpanRow[]
  rowId?: (spanId: string) => string
  focusedSpanId?: string | null
  onSelectSpan?: (spanId: string) => void
  className?: string
}) {
  const [active, setActive] = useState(0)
  const rows = useRef<(HTMLLIElement | null)[]>([])
  const last = spans.length - 1
  const tabbable = Math.min(Math.max(active, 0), Math.max(0, last))

  function move(event: KeyboardEvent<HTMLUListElement>) {
    let next: number
    if (event.key === 'ArrowDown') next = Math.min(last, tabbable + 1)
    else if (event.key === 'ArrowUp') next = Math.max(0, tabbable - 1)
    else if (event.key === 'Home') next = 0
    else if (event.key === 'End') next = last
    else return
    event.preventDefault()
    setActive(next)
    rows.current[next]?.focus()
  }

  return (
    <ul className={cn('space-y-0.5', className)} onKeyDown={move}>
      {spans.map((span, index) => {
        const focused = focusedSpanId === span.spanId
        return (
          <li
            key={span.spanId}
            id={rowId ? rowId(span.spanId) : undefined}
            ref={(node) => {
              rows.current[index] = node
            }}
            tabIndex={index === tabbable ? 0 : -1}
            aria-label={`${span.kind.replace('_', ' ')} ${span.name}, status ${span.status}`}
            onFocus={() => setActive(index)}
            onClick={onSelectSpan ? () => onSelectSpan(span.spanId) : undefined}
            className={cn(
              'rounded-sm text-xs outline-offset-[-2px] hover:bg-accent',
              focused && 'bg-accent/60 shadow-[inset_2px_0_0_var(--primary)]',
            )}
          >
            <div
              className="grid grid-cols-[16px_minmax(0,1fr)_auto_auto] items-center gap-2 py-1"
              style={{ paddingLeft: span.depth * 14 }}
            >
              <Tooltip>
                <TooltipTrigger asChild>
                  <span
                    className="tabular cursor-default text-center text-[13px]"
                    style={{ color: SPAN_STATUS_COLOR[span.status] }}
                  >
                    {SPAN_KIND_GLYPH[span.kind]}
                  </span>
                </TooltipTrigger>
                <TooltipContent>
                  {span.kind.replace('_', ' ')}: {span.status}
                </TooltipContent>
              </Tooltip>
              <span className="flex min-w-0 items-baseline gap-2">
                <span className="truncate">{span.name}</span>
                {span.clock ? (
                  <span className="tabular shrink-0 text-[11px] text-muted-foreground">
                    {span.clock}
                  </span>
                ) : null}
              </span>
              <span className="tabular text-[11px] text-muted-foreground">{span.tokens}</span>
              <span className="tabular flex items-center justify-end gap-2 text-right text-[11px] text-muted-foreground">
                {span.duration}
                {span.trailing}
              </span>
            </div>
            {span.content}
          </li>
        )
      })}
    </ul>
  )
}

const SEVERITY: Record<'info' | 'warning' | 'critical', { color: string; label: string }> = {
  info: { color: 'var(--primary)', label: 'Info' },
  warning: { color: 'var(--warning)', label: 'Warning' },
  critical: { color: 'var(--destructive)', label: 'Critical' },
}

export interface TraceInsight {
  kind: string
  severity: 'info' | 'warning' | 'critical'
  message: string
  spanId?: string | null
}

export function InsightList({
  insights,
  onSelectSpan,
  className,
}: {
  insights: TraceInsight[]
  onSelectSpan?: (spanId: string) => void
  className?: string
}) {
  return (
    <ul className={cn('space-y-1.5', className)}>
      {insights.map((insight, index) => {
        const severity = SEVERITY[insight.severity]
        const body = (
          <>
            <span
              aria-hidden
              className="mt-1.5 size-1.5 shrink-0 rounded-full"
              style={{ background: severity.color }}
            />
            <span className="min-w-0">
              <span className="font-medium" style={{ color: severity.color }}>
                {severity.label}
              </span>
              <span className="text-muted-foreground">
                {' '}
                ({insight.kind}): {insight.message}
              </span>
            </span>
          </>
        )

        const jumpable = insight.spanId && onSelectSpan
        return (
          <li key={`${insight.kind}-${index}`} className="text-xs leading-relaxed">
            {jumpable ? (
              <button
                type="button"
                onClick={() => onSelectSpan(insight.spanId as string)}
                className="flex w-full gap-2.5 rounded-sm text-left outline-offset-2 hover:bg-accent"
              >
                {body}
              </button>
            ) : (
              <span className="flex gap-2.5">{body}</span>
            )}
          </li>
        )
      })}
    </ul>
  )
}

const CAPABILITY_LABEL: Record<keyof Capabilities, string> = {
  trace: 'Trace',
  tokens: 'Tokens',
  cost: 'Cost',
  context: 'Context',
  latency: 'Latency',
}

export function CapabilityGrid({
  capabilities,
  className,
}: {
  capabilities: Capabilities
  className?: string
}) {
  const entries = Object.entries(capabilities) as [keyof Capabilities, Provenance][]

  return (
    <div className={cn('grid grid-cols-2 gap-x-4 gap-y-3 rounded-md border bg-muted/40 p-3', className)}>
      {entries.map(([key, provenance]) => (
        <div key={key} className="space-y-1">
          <StatLabel>{CAPABILITY_LABEL[key]}</StatLabel>
          <ProvenanceBadge provenance={provenance} />
        </div>
      ))}
    </div>
  )
}
