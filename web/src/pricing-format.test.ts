import { describe, expect, it } from 'vitest'
import {
  formatContextWindow,
  matchUnpriced,
  peakWindowText,
  providerLabel,
  stalenessBadge,
} from './pricing-format'

const none = { cache_read: null, cache_write_5m: null, cache_write_1h: null, input: 1, output: 1 }

describe('providerLabel', () => {
  it('maps known providers', () => {
    expect(providerLabel('openai')).toBe('OpenAI')
    expect(providerLabel('xai')).toBe('xAI')
    expect(providerLabel('github-copilot')).toBe('GitHub Copilot')
    expect(providerLabel('typesafe')).toBe('TypeSafe AI')
  })

  it('capitalises unknown providers', () => {
    expect(providerLabel('acme')).toBe('Acme')
  })
})

describe('formatContextWindow', () => {
  it('formats K and M', () => {
    expect(formatContextWindow(1_000_000)).toBe('1M')
    expect(formatContextWindow(272_000)).toBe('272K')
    expect(formatContextWindow(1_050_000)).toBe('1.05M')
    expect(formatContextWindow(200_000)).toBe('200K')
  })

  it('is null when unknown', () => {
    expect(formatContextWindow(null)).toBeNull()
  })
})

describe('peakWindowText', () => {
  it('compresses weekday runs and lists hour ranges in UTC', () => {
    expect(
      peakWindowText({
        weekdays: [0, 1, 2, 3, 4],
        utc_hours: [
          [1, 4],
          [6, 10],
        ],
        ...none,
      }),
    ).toBe('Mon-Fri 01:00-04:00, 06:00-10:00 UTC')
  })

  it('handles split weekday sets', () => {
    expect(peakWindowText({ weekdays: [0, 2, 3, 6], utc_hours: [[0, 24]], ...none })).toBe(
      'Mon, Wed-Thu, Sun 00:00-24:00 UTC',
    )
  })
})

describe('stalenessBadge', () => {
  it('has thresholds at 30 and 90 days', () => {
    expect(stalenessBadge(null)).toBeNull()
    expect(stalenessBadge(29)).toBeNull()
    expect(stalenessBadge(30)).toEqual({ level: 'info', text: '30+ days old' })
    expect(stalenessBadge(89)?.level).toBe('info')
    expect(stalenessBadge(90)).toEqual({ level: 'caution', text: '90+ days old; prices may have moved' })
  })
})

describe('matchUnpriced', () => {
  const entries = [
    { match: 'gemini-4', note: 'a', status: 'watchlist' as const },
    { match: 'Gemini-4-pro', note: 'b', status: null },
  ]

  it('prefers the longest prefix, case-insensitively', () => {
    expect(matchUnpriced('gemini-4-pro-preview', entries)?.note).toBe('b')
    expect(matchUnpriced('gemini-4-flash', entries)?.note).toBe('a')
  })

  it('returns null with no prefix match', () => {
    expect(matchUnpriced('gpt-9', entries)).toBeNull()
  })
})
