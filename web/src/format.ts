import type { SessionRow } from './api'

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

function trimMoney(scaled: number): string {
  const oneDecimal = scaled.toFixed(1)
  return Math.abs(Number(oneDecimal)) >= 10 ? scaled.toFixed(0) : oneDecimal
}

/** Axis ticks. Whole dollars stay whole (`$20`); fractional scales get cents
 *  (`$0.35`) so a tick never reads as a rounded lie. The sign is handled once,
 *  up front, so it never lands between the `$` and the digits. */
export function formatMoneyShort(value: number): string {
  const sign = value < 0 ? '-' : ''
  const abs = Math.abs(value)
  if (abs >= 1_000_000) return `${sign}$${trimMoney(abs / 1_000_000)}M`
  if (abs >= 1000) return `${sign}$${trimMoney(abs / 1000)}K`
  if (Number.isInteger(abs)) return `${sign}$${abs}`
  if (abs >= 10) return `${sign}$${Math.round(abs)}`
  return `${sign}$${abs.toFixed(2)}`
}

const TOKEN_UNITS: { threshold: number; suffix: string }[] = [
  { threshold: 1_000_000_000, suffix: 'B' },
  { threshold: 1_000_000, suffix: 'M' },
  { threshold: 1_000, suffix: 'K' },
]

/** `161.5M`, `4.9M`, `12.3K`. Exact value belongs in a title/tooltip. Rounds
 *  the scaled value first, then decides the unit, so a value that rounds up
 *  to the next unit's boundary is shown in that unit rather than as `1000M`. */
export function formatTokens(value: number): string {
  const sign = value < 0 ? '-' : ''
  const abs = Math.abs(value)
  for (const unit of TOKEN_UNITS) {
    const trimmed = trim(abs / unit.threshold)
    if (Number(trimmed) >= 1) return `${sign}${trimmed}${unit.suffix}`
  }
  return `${sign}${plain.format(Math.round(abs))}`
}

function trim(value: number): string {
  return value >= 100 ? value.toFixed(0) : value.toFixed(1)
}

/** `1 error`, `3 errors`. */
export function plural(count: number, word: string): string {
  return `${formatCount(count)} ${word}${count === 1 ? '' : 's'}`
}

export function formatCount(value: number): string {
  return plain.format(value)
}

/** `my-repo_267638e3-...`. Falls back to `(no project)` like the rest of the dashboard. */
export function sessionDisplayName(session: SessionRow): string {
  const name = session.project && session.project.trim() ? session.project : '(no project)'
  return `${name}_${session.session_id}`
}

export function formatExact(value: number): string {
  return `${plain.format(Math.round(value))} tokens`
}

export function formatDuration(ms: number): string {
  if (!Number.isFinite(ms) || ms < 0) return '--'
  if (ms < 999.5) return `${Math.round(ms)}ms`
  const seconds = ms / 1000
  if (seconds < 59.95) return `${seconds.toFixed(1)}s`
  const total = Math.round(seconds)
  const hours = Math.floor(total / 3600)
  const minutes = Math.floor((total % 3600) / 60)
  if (hours > 0) return `${hours}h ${String(minutes).padStart(2, '0')}m`
  return `${minutes}m ${String(total % 60).padStart(2, '0')}s`
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

const clock = new Intl.DateTimeFormat('en-GB', {
  hour: '2-digit',
  minute: '2-digit',
  hourCycle: 'h23',
})

export function formatClock(iso: string): string {
  const date = new Date(iso)
  if (Number.isNaN(date.getTime())) return iso
  return clock.format(date)
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

export const RECENCY_DAYS = 30

export function isRecent(lastSeen: string | undefined, today: string): boolean {
  if (!lastSeen) return false
  return lastSeen.slice(0, 10) >= shiftDays(today, -(RECENCY_DAYS - 1))
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

/** Last log record minus the first, elapsed time in ms, idle minutes included. */
export function logSpanMs(session: SessionRow): number {
  const start = Date.parse(session.start_time)
  const end = Date.parse(session.end_time)
  if (!Number.isFinite(start) || !Number.isFinite(end) || end <= start) return 0
  return end - start
}

/** Today's date in the viewer's own calendar, not UTC, so range presets and
 *  recency checks agree with what the viewer sees on their clock. */
export function today(): string {
  const now = new Date()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  return `${now.getFullYear()}-${month}-${day}`
}
