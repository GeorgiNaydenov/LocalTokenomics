import type { ReactNode } from 'react'

import type { CostState, OutcomeLabel, Provenance } from '@/api'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import { cn } from '@/design-system/cn'

const COST_STATE: Record<CostState, { label: string; color: string; help: string }> = {
  priced: {
    label: 'Priced',
    color: 'var(--state-priced)',
    help: 'A rate matched this model. Counted in every total.',
  },
  free: {
    label: 'Free',
    color: 'var(--state-free)',
    help: 'The provider is marked free, such as a local runtime. Counted at $0.00.',
  },
  unpriced: {
    label: 'Unpriced',
    color: 'var(--state-unpriced)',
    help: 'Tokens exist but no rate entry matches. Left out of cost totals.',
  },
  unavailable: {
    label: 'Unavailable',
    color: 'var(--state-unavailable)',
    help: 'The log carries no token counts. Cost is never invented.',
  },
}

const PROVENANCE: Record<Provenance, { label: string; color: string }> = {
  measured: { label: 'Measured', color: 'var(--provenance-measured)' },
  derived: { label: 'Derived', color: 'var(--provenance-derived)' },
  estimated: { label: 'Estimated', color: 'var(--provenance-estimated)' },
  inferred: { label: 'Inferred', color: 'var(--provenance-inferred)' },
  unavailable: { label: 'Unavailable', color: 'var(--provenance-unavailable)' },
}

const OUTCOME: Record<OutcomeLabel, { label: string; color: string; help: string }> = {
  successful: {
    label: 'Successful',
    color: 'var(--success)',
    help: 'The last turn completed and nothing was aborted.',
  },
  partial: {
    label: 'Partial',
    color: 'var(--warning)',
    help: 'Finished, but some tools were interrupted or retried.',
  },
  failed: {
    label: 'Failed',
    color: 'var(--destructive)',
    help: 'The last turn ended in an error.',
  },
  abandoned: {
    label: 'Abandoned',
    color: 'var(--chart-8)',
    help: 'The session stopped mid-turn and never resumed.',
  },
  unrated: {
    label: 'Unrated',
    color: 'var(--muted-foreground)',
    help: 'Not enough signal to judge, and never guessed.',
  },
}

function Dot({ color }: { color: string }) {
  return (
    <span
      aria-hidden
      className="size-1.5 shrink-0 rounded-full"
      style={{ background: color }}
    />
  )
}

export function Unavailable({ hint, className }: { hint?: string; className?: string }) {
  const word = (
    <span
      className={cn('whitespace-nowrap', className)}
      style={{ color: 'var(--state-unavailable)' }}
    >
      unavailable
    </span>
  )

  if (!hint) return word

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <span tabIndex={0} className="cursor-default rounded-sm outline-offset-2">
          {word}
        </span>
      </TooltipTrigger>
      <TooltipContent className="max-w-64">{hint}</TooltipContent>
    </Tooltip>
  )
}

export function PartialMarker({ hint }: { hint: string }) {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <span
          tabIndex={0}
          className="cursor-default rounded-sm text-[10px] text-muted-foreground outline-offset-2"
        >
          partial
        </span>
      </TooltipTrigger>
      <TooltipContent className="max-w-64">{hint}</TooltipContent>
    </Tooltip>
  )
}

function SignalBadge({
  color,
  label,
  prefix,
  title,
  className,
}: {
  color: string
  label: string
  prefix?: string
  title?: string
  className?: string
}) {
  const badge = (
    <span
      className={cn(
        'inline-flex w-fit shrink-0 items-center gap-1.5 rounded-full border px-2 py-0.5 text-xs font-medium whitespace-nowrap',
        title && 'cursor-default outline-offset-2',
        className,
      )}
      style={{ borderColor: `color-mix(in oklab, ${color} 35%, transparent)`, color }}
      tabIndex={title ? 0 : undefined}
    >
      <Dot color={color} />
      {prefix ? <span className="text-muted-foreground">{prefix}</span> : null}
      {label}
    </span>
  )

  if (!title) return badge

  return (
    <Tooltip>
      <TooltipTrigger asChild>{badge}</TooltipTrigger>
      <TooltipContent className="max-w-64">{title}</TooltipContent>
    </Tooltip>
  )
}

export function CostStateBadge({
  state,
  className,
}: {
  state: CostState
  className?: string
}) {
  const meta = COST_STATE[state]
  return (
    <SignalBadge
      color={meta.color}
      label={meta.label}
      title={meta.help}
      className={className}
    />
  )
}

export function ProvenanceBadge({
  provenance,
  group,
  title,
  className,
}: {
  provenance: Provenance
  group?: string
  title?: string
  className?: string
}) {
  const meta = PROVENANCE[provenance]
  return (
    <SignalBadge
      color={meta.color}
      label={meta.label}
      prefix={group}
      title={title}
      className={className}
    />
  )
}

export function OutcomeBadge({
  outcome,
  className,
}: {
  outcome: OutcomeLabel
  className?: string
}) {
  const meta = OUTCOME[outcome]
  return (
    <SignalBadge
      color={meta.color}
      label={meta.label}
      title={meta.help}
      className={className}
    />
  )
}

export function Meter({
  value,
  max = 1,
  color = 'var(--primary)',
  label,
  unavailableHint,
  className,
}: {
  value: number | null
  max?: number
  color?: string
  label?: string
  unavailableHint?: string
  className?: string
}) {
  if (value === null) {
    return (
      <div className={cn('flex h-1.5 items-center text-[11px]', className)}>
        <Unavailable hint={unavailableHint ?? label} />
      </div>
    )
  }

  const share = max > 0 ? Math.min(1, Math.max(0, value / max)) : 0
  return (
    <div
      role="meter"
      aria-valuenow={value}
      aria-valuemin={0}
      aria-valuemax={max}
      aria-label={label}
      className={cn('h-1.5 w-full overflow-hidden rounded-full bg-muted', className)}
    >
      <div
        className="h-full rounded-full transition-[width] duration-500"
        style={{ width: `${share * 100}%`, background: color }}
      />
    </div>
  )
}

export interface BucketSegment {
  key: string
  label: string
  value: number
  color: string
}

export function BucketBar({
  segments,
  formatValue,
  className,
}: {
  segments: BucketSegment[]
  formatValue?: (value: number) => string
  className?: string
}) {
  const total = segments.reduce((sum, segment) => sum + segment.value, 0)
  if (total <= 0) {
    return (
      <div className={cn('flex h-2 items-center text-[11px]', className)}>
        <Unavailable hint="No token counts in this log, so the mix cannot be shown." />
      </div>
    )
  }

  return (
    <div className={cn('flex h-2 w-full overflow-hidden rounded-full', className)}>
      {segments.map((segment) => (
        <Tooltip key={segment.key}>
          <TooltipTrigger asChild>
            <div
              tabIndex={0}
              aria-label={`${segment.label}, ${((segment.value / total) * 100).toFixed(1)} percent`}
              className="outline-offset-2 transition-opacity hover:opacity-80"
              style={{ width: `${(segment.value / total) * 100}%`, background: segment.color }}
            />
          </TooltipTrigger>
          <TooltipContent>
            <span className="tabular">
              {segment.label}: {((segment.value / total) * 100).toFixed(1)}%
              {formatValue ? `, ${formatValue(segment.value)}` : ''}
            </span>
          </TooltipContent>
        </Tooltip>
      ))}
    </div>
  )
}

export function Legend({
  items,
  className,
}: {
  items: { key: string; label: string; color: string; value?: string }[]
  className?: string
}) {
  return (
    <ul className={cn('flex flex-wrap items-center gap-x-4 gap-y-1.5', className)}>
      {items.map((item) => (
        <li key={item.key} className="flex items-center gap-1.5 text-xs">
          <Dot color={item.color} />
          <span className="text-muted-foreground">{item.label}</span>
          {item.value ? (
            <span className="tabular font-medium text-foreground">{item.value}</span>
          ) : null}
        </li>
      ))}
    </ul>
  )
}

export function MeterRow({
  label,
  meta,
  value,
  share,
  fraction,
  color = 'var(--primary)',
  labelWidth = 176,
  className,
}: {
  label: string
  meta?: string
  value: ReactNode
  share?: string
  fraction: number | null
  color?: string
  labelWidth?: number
  className?: string
}) {
  const width = fraction === null ? 0 : Math.min(100, Math.max(0, fraction * 100))

  return (
    <div
      className={cn('grid items-center gap-3 py-1.5', className)}
      style={{ gridTemplateColumns: `${labelWidth}px minmax(0,1fr) 84px` }}
    >
      <Tooltip>
        <TooltipTrigger asChild>
          <div tabIndex={0} className="min-w-0 cursor-default rounded-sm outline-offset-2">
            <div className="truncate text-[13px]">{label}</div>
            {meta ? (
              <div className="tabular truncate text-[11px] text-muted-foreground">{meta}</div>
            ) : null}
          </div>
        </TooltipTrigger>
        <TooltipContent>
          <span className="tabular">
            {label}: {value}
            {share ? `, ${share}` : ''}
            {meta ? `, ${meta}` : ''}
          </span>
        </TooltipContent>
      </Tooltip>
      <div className="relative">
        {fraction === null ? (
          <div className="flex h-3.5 items-center text-[11px]">
            <Unavailable hint={`No comparable value for ${label}, so no bar is drawn.`} />
          </div>
        ) : (
          <div className="h-3.5 overflow-hidden rounded-sm bg-muted">
            <div className="h-full rounded-sm transition-[width] duration-500" style={{ width: `${width}%`, background: color }} />
          </div>
        )}
        {fraction !== null && share ? (
          <span
            className="tabular pointer-events-none absolute top-0 text-[11px] leading-[14px] text-muted-foreground"
            style={{ left: `calc(${width}% + 6px)` }}
          >
            {share}
          </span>
        ) : null}
      </div>
      <div className="tabular text-right text-[13px] font-medium">{value}</div>
    </div>
  )
}

export function ComparisonMeter({
  caption,
  value,
  fraction,
  color = 'var(--primary)',
  className,
}: {
  caption?: string
  value: ReactNode
  fraction: number | null
  color?: string
  className?: string
}) {
  const width = fraction === null ? 0 : Math.min(100, Math.max(0, fraction * 100))
  const inside = width > 55

  if (fraction === null) {
    return (
      <div className={cn('space-y-1.5', className)}>
        {caption ? <p className="text-xs text-muted-foreground">{caption}</p> : null}
        <div className="flex h-7 items-center text-[13px]">
          <Unavailable hint={caption ? `No value logged for ${caption.toLowerCase()}.` : undefined} />
        </div>
      </div>
    )
  }

  return (
    <div className={cn('space-y-1.5', className)}>
      {caption ? <p className="text-xs text-muted-foreground">{caption}</p> : null}
      <div className="relative h-7 overflow-hidden rounded-sm bg-muted">
        <div className="h-full rounded-sm transition-[width] duration-500" style={{ width: `${width}%`, background: color }} />
        <span
          className={cn(
            'tabular absolute top-1/2 -translate-y-1/2 text-[13px] font-semibold',
            inside ? 'text-primary-foreground' : 'text-foreground',
          )}
          style={inside ? { right: 10 } : { left: `calc(${width}% + 8px)` }}
        >
          {value}
        </span>
      </div>
    </div>
  )
}

export const COST_STATE_META = COST_STATE
export const PROVENANCE_META = PROVENANCE
export const OUTCOME_META = OUTCOME
