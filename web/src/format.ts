const money = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})

const moneyPrecise = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 4,
})

const plain = new Intl.NumberFormat('en-US')

/** `$1,234.56` */
export function formatMoney(value: number): string {
  return money.format(value)
}

/** Keeps sub-cent figures from collapsing to `$0.00` in tooltips. */
export function formatMoneyExact(value: number): string {
  return value !== 0 && Math.abs(value) < 0.01 ? moneyPrecise.format(value) : money.format(value)
}

/** Axis ticks. Whole dollars stay whole (`$20`); fractional scales get cents
 *  (`$0.35`) so a tick never reads as a rounded lie. */
export function formatMoneyShort(value: number): string {
  const abs = Math.abs(value)
  if (abs >= 1000) return `$${(value / 1000).toFixed(abs >= 10_000 ? 0 : 1)}K`
  if (Number.isInteger(value)) return `$${value}`
  if (abs >= 10) return `$${Math.round(value)}`
  return `$${value.toFixed(2)}`
}

/** `161.5M`, `4.9M`, `12.3K`. Exact value belongs in a title/tooltip. */
export function formatTokens(value: number): string {
  const abs = Math.abs(value)
  if (abs >= 1_000_000_000) return `${trim(value / 1_000_000_000)}B`
  if (abs >= 1_000_000) return `${trim(value / 1_000_000)}M`
  if (abs >= 1_000) return `${trim(value / 1_000)}K`
  return plain.format(Math.round(value))
}

function trim(value: number): string {
  return value >= 100 ? value.toFixed(0) : value.toFixed(1)
}

export function formatCount(value: number): string {
  return plain.format(value)
}

export function formatExact(value: number): string {
  return `${plain.format(Math.round(value))} tokens`
}

export function formatPercent(value: number, digits = 0): string {
  return `${(value * 100).toFixed(digits)}%`
}

/** `2026-08-28` -> `Aug 28, 2026` (parsed as a plain date, never shifted by TZ). */
export function formatDay(iso: string, withYear = true): string {
  const [year, month, day] = iso.split('-').map(Number)
  if (!year || !month || !day) return iso
  const date = new Date(Date.UTC(year, month - 1, day))
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    ...(withYear ? { year: 'numeric' } : {}),
    timeZone: 'UTC',
  })
}

/** Axis tick: `Aug 28`. */
export function formatDayShort(iso: string): string {
  return formatDay(iso, false)
}

/** ISO timestamp -> `Aug 28, 2026, 6:18 PM` in the viewer's zone. */
export function formatTimestamp(iso: string | null): string {
  if (!iso) return '--'
  const date = new Date(iso)
  if (Number.isNaN(date.getTime())) return iso
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
}

export function formatDateRange(first: string | null, last: string | null): string {
  if (!first || !last) return 'no data'
  return first === last ? formatDay(first) : `${formatDay(first, false)} – ${formatDay(last)}`
}

export function toDayString(iso: string | null): string | null {
  return iso ? iso.slice(0, 10) : null
}

export function shiftDays(iso: string, days: number): string {
  const [year, month, day] = iso.split('-').map(Number)
  const date = new Date(Date.UTC(year, month - 1, day + days))
  return date.toISOString().slice(0, 10)
}

/** Inclusive list of every ISO day from `from` to `to`. */
export function daySpan(from: string, to: string): string[] {
  const days: string[] = []
  let cursor = from
  for (let guard = 0; guard < 4000 && cursor <= to; guard += 1) {
    days.push(cursor)
    cursor = shiftDays(cursor, 1)
  }
  return days
}
