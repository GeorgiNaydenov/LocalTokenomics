import { describe, expect, it } from 'vitest'

import {
  isEstimatedPriced,
  ratesAgeNotice,
  reportedDiverges,
  reportedNote,
  reportedTitle,
} from './pricing-notes'

describe('ratesAgeNotice', () => {
  it('is silent when fresh or unknown', () => {
    expect(ratesAgeNotice(null)).toBeNull()
    expect(ratesAgeNotice(29)).toBeNull()
  })
  it('is info from 30 days', () => {
    expect(ratesAgeNotice(30)).toEqual({
      severity: 'info',
      text: 'Prices are 30 days old: they may have moved. See Pricing.',
    })
    expect(ratesAgeNotice(89)?.severity).toBe('info')
  })
  it('is caution from 90 days', () => {
    expect(ratesAgeNotice(90)?.severity).toBe('caution')
    expect(ratesAgeNotice(200)?.text).toContain('200 days')
  })
})

describe('reportedDiverges', () => {
  it('ignores differences within 5% or one cent', () => {
    expect(reportedDiverges(10, 10.4)).toBe(false)
    expect(reportedDiverges(0.001, 0.01)).toBe(false)
  })
  it('flags larger differences', () => {
    expect(reportedDiverges(10, 11)).toBe(true)
    expect(reportedDiverges(0, 0.5)).toBe(true)
  })
})

describe('reportedNote', () => {
  it('returns null when no reported cost', () => {
    expect(reportedNote(1, null)).toBeNull()
    expect(reportedTitle(1, null)).toBeNull()
  })
  it('formats the line without a note when close', () => {
    expect(reportedNote(10, 10.1)).toEqual({ line: 'Reported by tool: $10.10', diverges: false, note: null })
  })
  it('adds the note when divergent', () => {
    expect(reportedNote(10, 20)?.note).toContain('rates.json')
    expect(reportedTitle(10, 20)).toContain('Reported by tool: $20.00.')
  })
})

describe('isEstimatedPriced', () => {
  const cost = { estimated: true }
  it('requires priced state and estimated cost', () => {
    expect(isEstimatedPriced('priced', cost)).toBe(true)
    expect(isEstimatedPriced('unpriced', cost)).toBe(false)
    expect(isEstimatedPriced('priced', { estimated: false })).toBe(false)
    expect(isEstimatedPriced('priced', null)).toBe(false)
  })
})
