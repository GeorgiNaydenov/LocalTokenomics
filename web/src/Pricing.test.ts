import { describe, expect, it } from 'vitest'
import type { Bucket, MatchKind, ModelRate, ProviderRules, RateTable, Report } from './api'
import { buildRow, estimatedModels, splitUnpriced } from './Pricing'

function rate(overrides: Partial<ModelRate> = {}): ModelRate {
  return {
    match: 'claude-x',
    provider: 'anthropic',
    display: 'Claude X',
    input: 3,
    output: 15,
    cache_read: null,
    cache_write_5m: null,
    cache_write_1h: null,
    variants: {},
    bands: [],
    peak: null,
    periods: [],
    cache_rules: null,
    context_window: null,
    source: null,
    verified: '2026-10-01',
    status: 'ga',
    released: null,
    retired: null,
    note: null,
    estimated: false,
    inherited: false,
    match_kind: null,
    ...overrides,
  }
}

function bucket(key: string, cost: number, label = key): Bucket {
  return {
    key,
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
      total: 100,
    },
    cost: {
      uncached_input: 0,
      cache_read: 0,
      cache_write: 0,
      output: 0,
      no_cache_equivalent: 0,
      total: cost,
      cache_savings: 0,
      inherited: false,
      estimated: false,
    },
    events: 0,
    sessions: 0,
    reported_cost: null,
  }
}

const RULES: ProviderRules = {
  cache_read: 0.1,
  cache_write_5m: 1.25,
  cache_write_1h: 2,
  batch: 0.5,
  free: false,
}

function ratesWith(models: ModelRate[], providers: Record<string, ProviderRules> = { anthropic: RULES }): RateTable {
  return {
    as_of: '2026-10-01',
    currency: 'USD',
    units: 'per million tokens',
    notes: [],
    prefixes: [],
    providers,
    models,
    unpriced_models: [],
  }
}

function reportWith(buckets: Bucket[], matches: Record<string, [string | null, MatchKind]> = {}): Report {
  const model_matches: Report['model_matches'] = {}
  for (const b of buckets) {
    const entry = matches[b.key]
    model_matches[b.key] = entry ? { match: entry[0], kind: entry[1] } : { match: null, kind: 'none' }
  }
  return { by_model: buckets, model_matches, unknown_models: [] } as unknown as Report
}

describe('buildRow spend join by model key', () => {
  it('sums every bucket matched to this row', () => {
    const r = rate()
    const report = reportWith([bucket('a', 1.5), bucket('b', 2.5)], {
      a: ['claude-x', 'exact'],
      b: ['claude-x', 'suffix'],
    })
    expect(buildRow(r, ratesWith([r]), report).spendValue).toBe(4)
  })

  it('ignores buckets matched to another row', () => {
    const r = rate()
    const report = reportWith([bucket('a', 1.5), bucket('b', 9)], {
      a: ['claude-x', 'exact'],
      b: ['claude-y', 'exact'],
    })
    expect(buildRow(r, ratesWith([r]), report).spendValue).toBe(1.5)
  })

  it('does not collide when two rows share a display label', () => {
    const one = rate({ match: 'x-one', display: 'Same' })
    const two = rate({ match: 'x-two', display: 'Same' })
    const report = reportWith([bucket('x-one', 1, 'Same'), bucket('x-two', 5, 'Same')], {
      'x-one': ['x-one', 'exact'],
      'x-two': ['x-two', 'exact'],
    })
    const table = ratesWith([one, two])
    expect(buildRow(one, table, report).spendValue).toBe(1)
    expect(buildRow(two, table, report).spendValue).toBe(5)
  })

  it('does not credit an estimated bucket to the parent, and lists it separately', () => {
    const r = rate()
    const report = reportWith([bucket('claude-x', 2), bucket('claude-x-9', 7)], {
      'claude-x': ['claude-x', 'exact'],
      'claude-x-9': ['claude-x', 'estimated'],
    })
    const row = buildRow(r, ratesWith([r]), report)
    expect(row.spendValue).toBe(2)
    expect(row.estimated).toEqual([
      { model: 'claude-x-9', parentMatch: 'claude-x', parentDisplay: 'Claude X', tokens: 100, cost: 7 },
    ])
  })

  it('reports unused with zero spend when nothing matches', () => {
    const r = rate()
    const row = buildRow(r, ratesWith([r]), reportWith([]))
    expect(row.spendValue).toBe(0)
    expect(row.state).toBe('unused')
  })
})

describe('estimatedModels', () => {
  it('only returns estimated matches, biggest cost first', () => {
    const r = rate()
    const report = reportWith([bucket('a', 1), bucket('b', 3), bucket('c', 5)], {
      a: ['claude-x', 'exact'],
      b: ['claude-x', 'estimated'],
      c: ['claude-x', 'estimated'],
    })
    expect(estimatedModels(ratesWith([r]), report).map((m) => m.model)).toEqual(['c', 'b'])
  })
})

describe('buildRow cache columns', () => {
  it('derives cache prices from the provider rules', () => {
    const r = rate()
    const row = buildRow(r, ratesWith([r]), reportWith([]))
    expect([row.cacheRead, row.cacheWrite5m, row.cacheWrite1h]).toEqual(['$0.300', '$3.750', '$6.000'])
  })

  it('prefers absolute prices the row publishes', () => {
    const r = rate({ cache_read: 0.25, cache_write_5m: 4, cache_write_1h: 7 })
    const row = buildRow(r, ratesWith([r]), reportWith([]))
    expect([row.cacheRead, row.cacheWrite5m, row.cacheWrite1h]).toEqual(['$0.250', '$4.000', '$7.000'])
  })

  it('mixes absolute and derived per field', () => {
    const r = rate({ cache_read: 0.25 })
    const row = buildRow(r, ratesWith([r]), reportWith([]))
    expect(row.cacheRead).toBe('$0.250')
    expect(row.cacheWrite5m).toBe('$3.750')
  })

  it('keeps provider fields when cache_rules is partial', () => {
    const r = rate({
      cache_rules: { cache_read: 0.5, cache_write_5m: null, cache_write_1h: null, batch: null, free: null },
    })
    const row = buildRow(r, ratesWith([r]), reportWith([]))
    expect(row.cacheRead).toBe('$1.500')
    expect(row.cacheWrite5m).toBe('$3.750')
  })

  it('is unavailable (null) with no provider block and no absolute price', () => {
    const r = rate({ provider: 'nobody', cache_read: 0.3 })
    const row = buildRow(r, ratesWith([r]), reportWith([]))
    expect(row.cacheRead).toBe('$0.300')
    expect(row.cacheWrite5m).toBeNull()
    expect(row.cacheWrite1h).toBeNull()
  })

  it('shows free for a free provider', () => {
    const r = rate({ provider: 'local' })
    const table = ratesWith([r], { local: { ...RULES, free: true } })
    const row = buildRow(r, table, reportWith([]))
    expect(row.input).toBe('free')
    expect(row.cacheRead).toBe('free')
    expect(row.state).toBe('free')
  })
})

describe('buildRow metadata', () => {
  it('formats the context window', () => {
    const r = rate({ context_window: 272_000 })
    expect(buildRow(r, ratesWith([r]), reportWith([])).contextWindow).toBe('272K')
  })

  it('lists variants with prices', () => {
    const r = rate({
      variants: {
        fast: { input: 6, output: 30, cache_read: null, cache_write_5m: null, cache_write_1h: null },
      },
    })
    expect(buildRow(r, ratesWith([r]), reportWith([])).variants).toEqual([
      { tier: 'fast', text: '$6.00 in / $30.00 out' },
    ])
  })

  it('carries band, peak and period detail strings', () => {
    const none = { cache_read: null, cache_write_5m: null, cache_write_1h: null }
    const r = rate({
      bands: [{ min_input_tokens: 272_001, input: 6, output: 22.5, variants: null, ...none }],
      peak: { weekdays: [0, 1, 2, 3, 4], utc_hours: [[1, 4]], input: 4, output: 16, ...none },
      periods: [
        { from: '2026-01-01', until: '2026-03-01', input: 2, output: null, variants: null, bands: null, peak: null, ...none },
      ],
    })
    const row = buildRow(r, ratesWith([r]), reportWith([]))
    expect(row.bands).toEqual(['from 272,001 input tokens: $6.00 in / $22.50 out'])
    expect(row.peak).toBe('Mon-Fri 01:00-04:00 UTC: $4.00 in / $16.00 out')
    expect(row.periods).toEqual(['2026-01-01 to 2026-03-01: $2.00 in / $15.00 out'])
  })

  it('tags preview, retired and unverified rows', () => {
    const r = rate({ status: 'preview', verified: null })
    expect(buildRow(r, ratesWith([r]), reportWith([])).tags.map((t) => t.key)).toEqual(['preview', 'unverified'])
  })
})

describe('splitUnpriced', () => {
  const entries = [
    { match: 'gemini-4', note: 'general note', status: 'watchlist' as const },
    { match: 'gemini-4-pro', note: 'pro note', status: 'no_list_price' as const },
    { match: 'gemini-5', note: 'idle', status: 'watchlist' as const },
  ]

  it('matches the longest prefix and separates truly unknown models', () => {
    const models = [
      { model: 'gemini-4-pro-exp', tokens: 1, events: 1 },
      { model: 'mystery', tokens: 1, events: 1 },
    ]
    const split = splitUnpriced(models, entries)
    expect(split.listed.map((l) => l.entry.match)).toEqual(['gemini-4-pro'])
    expect(split.unknown.map((m) => m.model)).toEqual(['mystery'])
    expect(split.idle.map((e) => e.match)).toEqual(['gemini-4', 'gemini-5'])
  })
})
