import type { Totals } from '../api'
import { formatMoney, formatPercent } from '../format'
import { Card, CardHeader } from './Card'

/** One hue, two steps: the meter reads as "of the full bill, this much was paid". */
export function CacheSavings({ totals }: { totals: Totals }) {
  const { cache_savings: saved, no_cache_equivalent: full, total: billed } = totals.cost
  const denominator = full > 0 ? full : billed
  const billedShare = denominator > 0 ? billed / denominator : 0
  const savedShare = denominator > 0 ? saved / denominator : 0

  return (
    <Card>
      <CardHeader
        title="Prompt caching"
        hint={
          saved > 0 ? (
            <>
              Prompt caching saved <strong className="font-semibold text-ink">{formatMoney(saved)}</strong> — these
              tokens would have cost {formatMoney(full)} without it.
            </>
          ) : (
            'No cache reads in this slice, so nothing was saved by caching.'
          )
        }
      />

      <div
        className="flex h-6 w-full gap-0.5 overflow-hidden rounded-md"
        role="img"
        aria-label={`Billed ${formatMoney(billed)} of a ${formatMoney(full)} uncached equivalent; ${formatMoney(saved)} saved`}
      >
        <span
          className="h-full"
          style={{
            width: `${Math.max(billedShare * 100, 0.5)}%`,
            background: 'var(--meter-fill)',
          }}
        />
        <span
          className="h-full flex-1"
          style={{ background: 'var(--meter-track)' }}
        />
      </div>

      <div className="mt-3 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <Figure
          swatch="var(--meter-fill)"
          label="Actually billed"
          value={formatMoney(billed)}
          note={formatPercent(billedShare)}
        />
        <Figure
          swatch="var(--meter-track)"
          label="Saved by caching"
          value={formatMoney(saved)}
          note={formatPercent(savedShare)}
        />
        <Figure
          swatch="transparent"
          label="Uncached equivalent"
          value={formatMoney(full)}
          note="every token at full input price"
        />
      </div>
    </Card>
  )
}

interface FigureProps {
  swatch: string
  label: string
  value: string
  note: string
}

function Figure({ swatch, label, value, note }: FigureProps) {
  return (
    <div>
      <p className="flex items-center gap-1.5 text-[12px] text-ink-2">
        <span
          aria-hidden
          className="inline-block h-2.5 w-2.5 shrink-0 rounded-[3px]"
          style={{ background: swatch, boxShadow: swatch === 'transparent' ? 'inset 0 0 0 1.5px var(--axis)' : undefined }}
        />
        {label}
      </p>
      <p className="mt-1 text-[22px] leading-none font-semibold tracking-tight text-ink">{value}</p>
      <p className="mt-1.5 text-[12px] text-muted">{note}</p>
    </div>
  )
}
