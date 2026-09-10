import { describe, expect, it } from 'vitest'
import type { SessionRow } from './api'
import {
  daySpan,
  formatClock,
  formatDay,
  formatDuration,
  formatMoney,
  formatMoneyExact,
  formatMoneyShort,
  formatPercent,
  formatTimestamp,
  formatTokens,
  logSpanMs,
  plural,
  shiftDays,
  today,
} from './format'

describe('formatMoney', () => {
  it('formats whole dollars with two decimal places', () => {
    expect(formatMoney(1234.5)).toBe('$1,234.50')
  })
})

describe('formatMoneyExact', () => {
  it('keeps four decimal places for a sub-cent value instead of collapsing to $0.00', () => {
    expect(formatMoneyExact(0.0025)).toBe('$0.0025')
  })

  it('falls back to two decimal places once a cent is reached', () => {
    expect(formatMoneyExact(0.5)).toBe('$0.50')
  })

  it('renders exactly zero as $0.00, not four decimal places', () => {
    expect(formatMoneyExact(0)).toBe('$0.00')
  })
})

describe('formatTokens', () => {
  it('abbreviates millions', () => {
    expect(formatTokens(4_900_000)).toBe('4.9M')
  })

  it('renders small counts as-is', () => {
    expect(formatTokens(42)).toBe('42')
  })

  it('rolls 999,999 tokens up to the next unit instead of "1000K"', () => {
    expect(formatTokens(999_999)).toBe('1.0M')
  })

  it('rolls 999,999,999 tokens up to the next unit instead of "1000M"', () => {
    expect(formatTokens(999_999_999)).toBe('1.0B')
  })

  it('does not promote a value that legitimately rounds within its unit', () => {
    expect(formatTokens(1_249_999_999)).toBe('1.2B')
  })

  it('handles negative values with the sign in front', () => {
    expect(formatTokens(-999_999)).toBe('-1.0M')
  })

  it('formats zero as a plain count', () => {
    expect(formatTokens(0)).toBe('0')
  })
})

describe('formatMoneyShort', () => {
  it('gains a millions branch instead of stopping at K', () => {
    expect(formatMoneyShort(1_000_000)).toBe('$1.0M')
  })

  it('places a negative sign before the dollar sign, not after', () => {
    expect(formatMoneyShort(-0.5)).toBe('-$0.50')
  })

  it('rounds a negative two-digit value to a whole number', () => {
    expect(formatMoneyShort(-12.4)).toBe('-$12')
  })

  it('promotes a value that rounds up to a whole ten-thousands figure', () => {
    expect(formatMoneyShort(9999)).toBe('$10K')
  })

  it('keeps a whole dollar amount unscaled', () => {
    expect(formatMoneyShort(20)).toBe('$20')
  })

  it('keeps a fractional amount under $10 in cents', () => {
    expect(formatMoneyShort(0.35)).toBe('$0.35')
  })
})

describe('formatDuration', () => {
  it('renders sub-second durations in ms', () => {
    expect(formatDuration(500)).toBe('500ms')
  })

  it('returns a placeholder for invalid input', () => {
    expect(formatDuration(-1)).toBe('--')
    expect(formatDuration(Number.NaN)).toBe('--')
  })
})

describe('formatPercent', () => {
  it('formats a ratio as a whole-number percentage by default', () => {
    expect(formatPercent(0.256)).toBe('26%')
  })

  it('honors the requested digit count', () => {
    expect(formatPercent(0.256, 1)).toBe('25.6%')
  })
})

describe('plural', () => {
  it('keeps the singular form for a count of one', () => {
    expect(plural(1, 'error')).toBe('1 error')
  })

  it('adds an s for every other count', () => {
    expect(plural(0, 'error')).toBe('0 errors')
    expect(plural(3, 'error')).toBe('3 errors')
  })

  it('formats the count with thousands separators', () => {
    expect(plural(1234, 'session')).toBe('1,234 sessions')
  })
})

function sessionWithSpan(start: string, end: string): SessionRow {
  return { start_time: start, end_time: end } as unknown as SessionRow
}

describe('logSpanMs', () => {
  it('returns the gap between the first and last record', () => {
    const session = sessionWithSpan('2026-01-01T00:00:00Z', '2026-01-01T01:00:00Z')
    expect(logSpanMs(session)).toBe(60 * 60 * 1000)
  })

  it('returns zero when the end is not after the start', () => {
    const session = sessionWithSpan('2026-01-01T01:00:00Z', '2026-01-01T00:00:00Z')
    expect(logSpanMs(session)).toBe(0)
  })

  it('returns zero for an unparsable timestamp instead of NaN', () => {
    const session = sessionWithSpan('not a date', '2026-01-01T00:00:00Z')
    expect(logSpanMs(session)).toBe(0)
  })
})

describe('today', () => {
  it('returns an ISO date string in the local calendar', () => {
    const now = new Date()
    const expected = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`
    expect(today()).toBe(expected)
  })
})

describe('formatDay', () => {
  it('parses the ISO day as a plain date, never shifted by the viewer\'s time zone', () => {
    expect(formatDay('2026-08-28')).toBe('Aug 28, 2026')
  })

  it('can omit the year', () => {
    expect(formatDay('2026-08-28', false)).toBe('Aug 28')
  })
})

describe('shiftDays', () => {
  it('moves forward across a month boundary using UTC arithmetic', () => {
    expect(shiftDays('2026-01-31', 1)).toBe('2026-02-01')
  })

  it('moves backward across a year boundary', () => {
    expect(shiftDays('2026-01-01', -1)).toBe('2025-12-31')
  })
})

describe('formatTimestamp and formatClock', () => {
  it('both return a placeholder for an unparsable timestamp', () => {
    expect(formatTimestamp('not a date')).toBe('not a date')
    expect(formatClock('not a date')).toBe('not a date')
  })

  it('formatTimestamp returns a placeholder for a null input', () => {
    expect(formatTimestamp(null)).toBe('--')
  })
})

describe('daySpan', () => {
  it('lists every day inclusive of both ends', () => {
    expect(daySpan('2026-01-01', '2026-01-03')).toEqual(['2026-01-01', '2026-01-02', '2026-01-03'])
  })

  it('returns a single day when from equals to', () => {
    expect(daySpan('2026-01-01', '2026-01-01')).toEqual(['2026-01-01'])
  })
})
