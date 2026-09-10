import * as React from 'react'
import { useEffect, useRef, useState } from 'react'

import { InfoGlyph, MetricInfo, type MetricInfoContent } from '@/components/metric-info'
import { cn } from '@/design-system/cn'

function reducedMotion() {
  return (
    typeof window !== 'undefined' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  )
}

export function NumberTicker({
  value,
  format,
  duration = 650,
  className,
}: {
  value: number
  format: (value: number) => string
  duration?: number
  className?: string
}) {
  const [shown, setShown] = useState(value)
  const origin = useRef(value)

  useEffect(() => {
    if (reducedMotion()) {
      origin.current = value
      setShown(value)
      return
    }
    const from = origin.current
    const start = performance.now()
    let frame = requestAnimationFrame(function step(now) {
      const progress = Math.min(1, (now - start) / duration)
      const eased = 1 - Math.pow(1 - progress, 3)
      setShown(from + (value - from) * eased)
      if (progress < 1) frame = requestAnimationFrame(step)
      else origin.current = value
    })
    return () => cancelAnimationFrame(frame)
  }, [value, duration])

  return <span className={cn('tabular', className)}>{format(shown)}</span>
}

export function StatLabel({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      className={cn(
        'text-[11px] font-medium uppercase tracking-[0.08em] text-muted-foreground',
        className,
      )}
      {...props}
    />
  )
}

export function Stat({
  label,
  value,
  format,
  unit,
  hint,
  info,
  exact,
  emphasis = 'default',
  className,
  children,
  onClick,
}: {
  label: string
  value: React.ReactNode
  format?: (value: number) => string
  unit?: string
  hint?: React.ReactNode
  /** Rich on-demand explanation (meaning, formula, live-value formula, provenance,
   *  caveats), opened from a small (i) glyph next to the label on hover, focus and tap. */
  info?: MetricInfoContent
  /** The full, unrounded value, shown inside the info box so an abbreviated headline
   *  number (e.g. "1.2B") never hides the true count. */
  exact?: string
  emphasis?: 'default' | 'hero'
  className?: string
  children?: React.ReactNode
  onClick?: () => void
}) {
  const infoContent: MetricInfoContent | undefined =
    info && exact
      ? info.kind === 'metric'
        ? { ...info, computed: info.computed ? `${info.computed}\nExact: ${exact}` : `Exact: ${exact}` }
        : { kind: 'metric', meaning: info.text, computed: `Exact: ${exact}` }
      : info
  const content = (
    <>
      <div className="flex items-center gap-1.5">
        <StatLabel>{label}</StatLabel>
        {infoContent ? (
          <MetricInfo content={infoContent} ariaLabel={`Explain ${label}`}>
            <InfoGlyph />
          </MetricInfo>
        ) : null}
      </div>
      <div className="flex flex-wrap items-baseline gap-x-1.5 gap-y-1">
        <span
          className={cn(
            'tabular min-w-0 font-semibold leading-none tracking-[-0.02em] text-card-foreground',
            emphasis === 'hero' ? 'text-[2.5rem]' : 'text-2xl',
          )}
        >
          {typeof value === 'number' && format ? (
            <NumberTicker value={value} format={format} />
          ) : (
            value
          )}
        </span>
        {unit ? (
          <span className="text-sm font-medium text-muted-foreground">{unit}</span>
        ) : null}
      </div>
      {hint ? <p className="text-xs leading-relaxed text-muted-foreground">{hint}</p> : null}
      {children}
    </>
  )
  const cardClassName = cn(
    'flex min-w-0 flex-col justify-between gap-3 rounded-md border bg-card p-card',
    onClick && 'cursor-pointer text-left outline-offset-2 hover:border-primary/50 hover:bg-accent/40',
    className,
  )
  if (onClick) {
    // A `role="button"` div rather than a native <button>: `info` renders its own
    // focusable, keyboard-operable trigger inside the card, and a native button cannot
    // contain another interactive element without breaking HTML nesting rules.
    return (
      <div
        role="button"
        tabIndex={0}
        onClick={onClick}
        onKeyDown={(event) => {
          if (event.target !== event.currentTarget) return
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault()
            onClick()
          }
        }}
        className={cardClassName}
      >
        {content}
      </div>
    )
  }
  return <div className={cardClassName}>{content}</div>
}

export function StatGrid({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      className={cn('grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4', className)}
      {...props}
    />
  )
}
