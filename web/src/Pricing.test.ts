import { describe, expect, it } from 'vitest'
import type { Bucket, ModelRate, RateTable, Report } from './api'
import { buildRow } from './Pricing'

function rate(overrides: Partial<ModelRate> = {}): ModelRate {
  return {
    match: 'claude-x',
    provider: 'anthropic',
    display: 'Claude X',
    input: 3,
    output: 15,
    variants: {},
    cache_rules: null,
    context_window: null,
    inherited: false,
    ...overrides,
  }
}

function bucket(label: string, cost: number): Bucket {
  return {
    key: label,
    label,
    tokens: {
      uncached_input: 0,
      cache_read: 0,
      cache_write_5m: 0,
      cache_write_1h: 0,
      output: 0,
      reasoning_output: 0,
      cache_write: 0,
      input_total: 0,
      total: 0,
    },
    cost: {
      uncached_input: 0,
      cache_read: 0,
      cache_write: 0,
      output: 0,
      no_cache_equivalent: 0,
      total: cost,
      cache_savings: 0,
    },
    events: 0,
    sessions: 0,
  }
}

function ratesWith(models: ModelRate[]): RateTable {
  return {
    as_of: '2026-01-01',
    currency: 'USD',
    units: 'per million tokens',
    notes: [],
    prefixes: [],
    providers: {},
    models,
  }
}

function reportWith(buckets: Bucket[]): Report {
  return { by_model: buckets } as unknown as Report
}

describe('buildRow spend aggregation', () => {
  it('sums every by_model bucket that shares this rate\'s display label', () => {
    const modelRate = rate({ display: 'Claude X' })
    const report = reportWith([bucket('Claude X', 1.5), bucket('Claude X', 2.5)])
    const row = buildRow(modelRate, ratesWith([modelRate]), report)
    expect(row.spendValue).toBe(4)
  })

  it('does not attribute spend from a bucket with a different label', () => {
    const modelRate = rate({ display: 'Claude X' })
    const report = reportWith([bucket('Claude X', 1.5), bucket('Claude Y', 9)])
    const row = buildRow(modelRate, ratesWith([modelRate]), report)
    expect(row.spendValue).toBe(1.5)
  })

  it('reports zero spend, state unused, when no bucket matches', () => {
    const modelRate = rate({ display: 'Claude X' })
    const row = buildRow(modelRate, ratesWith([modelRate]), reportWith([]))
    expect(row.spendValue).toBe(0)
    expect(row.state).toBe('unused')
  })
})

describe('buildRow variant tiers', () => {
  it('lists every declared variant tier', () => {
    const modelRate = rate({
      variants: {
        'long-context': { input: 6, output: 22.5 },
        batch: { input: 1.5, output: 7.5 },
      },
    })
    const row = buildRow(modelRate, ratesWith([modelRate]), reportWith([]))
    expect(row.variants).toEqual([
      { tier: 'long-context', input: '$6.00', output: '$22.50' },
      { tier: 'batch', input: '$1.50', output: '$7.50' },
    ])
  })

  it('is empty when the rate carries no variants', () => {
    const modelRate = rate()
    const row = buildRow(modelRate, ratesWith([modelRate]), reportWith([]))
    expect(row.variants).toEqual([])
  })
})
