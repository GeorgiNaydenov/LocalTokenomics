import { describe, expect, it } from 'vitest'
import type { EconRow } from './api'
import {
  UNATTRIBUTED_TURN_KEY,
  UNATTRIBUTED_TURN_LABEL,
  costConcentration,
  errorOrRetryTurns,
  halfCostTrend,
  longestTurn,
  realTurns,
  sortRealTurns,
  toolHeaviestTurn,
  truncateLabel,
  turnLabel,
  unattributedCostShare,
} from './turn-insights'

function row(overrides: Partial<EconRow> = {}): EconRow {
  return {
    key: 'turn-1',
    label: null,
    ordinal: 1,
    started_at: null,
    is_sidechain: false,
    model_calls: 1,
    tool_calls: 0,
    tokens: null,
    tokens_provenance: 'unavailable',
    cost: null,
    cost_state: 'unavailable',
    duration_ms: null,
    duration_provenance: 'unavailable',
    errors: 0,
    retries: null,
    amplification: null,
    cache_hit_ratio: null,
    tokens_per_second: null,
    ...overrides,
  }
}

function cost(total: number) {
  return {
    uncached_input: 0,
    cache_read: 0,
    cache_write: 0,
    output: total,
    total,
    no_cache_equivalent: total,
    cache_savings: 0,
    inherited: false,
  }
}

describe('truncateLabel', () => {
  it('leaves a short label untouched', () => {
    expect(truncateLabel('fix the bug', 40)).toBe('fix the bug')
  })

  it('cuts a long label to the limit and appends an ellipsis', () => {
    const label = 'a'.repeat(60)
    const truncated = truncateLabel(label, 40)
    expect(truncated).toBe(`${'a'.repeat(40)}…`)
  })

  it('never appends an ellipsis when the label exactly fits', () => {
    expect(truncateLabel('a'.repeat(40), 40)).toBe('a'.repeat(40))
  })
})

describe('turnLabel', () => {
  it('formats an ordinal with a quoted, truncated snippet', () => {
    expect(turnLabel(row({ ordinal: 7, label: 'refactor the pricing table' }))).toBe(
      'Turn 7 · "refactor the pricing table"',
    )
  })

  it('falls back to just the ordinal when the label is null, never an empty quoted string', () => {
    expect(turnLabel(row({ ordinal: 3, label: null }))).toBe('Turn 3')
  })

  it('shows the unattributed row label unchanged, not an ordinal', () => {
    expect(turnLabel(row({ key: UNATTRIBUTED_TURN_KEY, ordinal: null, label: UNATTRIBUTED_TURN_LABEL }))).toBe(
      UNATTRIBUTED_TURN_LABEL,
    )
  })
})

describe('realTurns', () => {
  it('excludes the unattributed row', () => {
    const rows = [row({ key: 'a' }), row({ key: UNATTRIBUTED_TURN_KEY }), row({ key: 'b' })]
    expect(realTurns(rows).map((r) => r.key)).toEqual(['a', 'b'])
  })
})

describe('sortRealTurns', () => {
  const rows = [
    row({ key: 'a', ordinal: 1, cost: cost(1), duration_ms: 300, errors: 0 }),
    row({ key: UNATTRIBUTED_TURN_KEY, ordinal: null, cost: cost(999), duration_ms: 999999, errors: 99 }),
    row({ key: 'b', ordinal: 2, cost: cost(5), duration_ms: 100, errors: 2 }),
  ]

  it('excludes the unattributed row from ordinal sorting entirely, not just ranks it last', () => {
    const sorted = sortRealTurns(rows, 'ordinal', 'asc')
    expect(sorted.map((r) => r.key)).toEqual(['a', 'b'])
  })

  it('sorts by cost descending', () => {
    expect(sortRealTurns(rows, 'cost', 'desc').map((r) => r.key)).toEqual(['b', 'a'])
  })

  it('sorts by duration ascending', () => {
    expect(sortRealTurns(rows, 'duration', 'asc').map((r) => r.key)).toEqual(['b', 'a'])
  })

  it('sorts by errors descending', () => {
    expect(sortRealTurns(rows, 'errors', 'desc').map((r) => r.key)).toEqual(['b', 'a'])
  })
})

describe('costConcentration', () => {
  it('is null when no turn carries a priced cost', () => {
    expect(costConcentration([row({ cost: null })])).toBeNull()
  })

  it('computes the top-N share against the sum of turn cost, not the unattributed row', () => {
    const rows = [
      row({ key: 'a', cost: cost(10) }),
      row({ key: 'b', cost: cost(30) }),
      row({ key: 'c', cost: cost(60) }),
      row({ key: UNATTRIBUTED_TURN_KEY, cost: cost(1000) }),
    ]
    const result = costConcentration(rows, 2)
    expect(result).not.toBeNull()
    expect(result?.totalTurnCost).toBe(100)
    expect(result?.topCost).toBe(90)
    expect(result?.share).toBeCloseTo(0.9)
    expect(result?.topRows.map((r) => r.key)).toEqual(['c', 'b'])
  })
})

describe('longestTurn', () => {
  it('picks the turn with the largest known duration, ignoring turns with no duration', () => {
    const rows = [
      row({ key: 'a', duration_ms: 500 }),
      row({ key: 'b', duration_ms: null }),
      row({ key: 'c', duration_ms: 4000 }),
    ]
    expect(longestTurn(rows)?.key).toBe('c')
  })

  it('is null when no turn has a known duration', () => {
    expect(longestTurn([row({ duration_ms: null })])).toBeNull()
  })
})

describe('errorOrRetryTurns', () => {
  it('counts turns with an error or a retry and finds the worst by errors first', () => {
    const rows = [
      row({ key: 'a', errors: 1, retries: 0 }),
      row({ key: 'b', errors: 0, retries: 2 }),
      row({ key: 'c', errors: 3, retries: 1 }),
      row({ key: 'd', errors: 0, retries: null }),
    ]
    const result = errorOrRetryTurns(rows)
    expect(result.count).toBe(3)
    expect(result.worst?.key).toBe('c')
  })

  it('is empty when nothing has an error or a retry', () => {
    expect(errorOrRetryTurns([row({ errors: 0, retries: null })])).toEqual({ count: 0, worst: null })
  })
})

describe('toolHeaviestTurn', () => {
  it('picks the turn with the most tool calls', () => {
    const rows = [row({ key: 'a', tool_calls: 2 }), row({ key: 'b', tool_calls: 9 })]
    expect(toolHeaviestTurn(rows)?.key).toBe('b')
  })

  it('is null when no turn made a tool call', () => {
    expect(toolHeaviestTurn([row({ tool_calls: 0 })])).toBeNull()
  })
})

describe('halfCostTrend', () => {
  it('is null with fewer than two turns', () => {
    expect(halfCostTrend([row()])).toBeNull()
  })

  it('splits by ordinal into two halves and sums each half separately', () => {
    const rows = [
      row({ key: 'a', ordinal: 1, cost: cost(10) }),
      row({ key: 'b', ordinal: 2, cost: cost(20) }),
      row({ key: 'c', ordinal: 3, cost: cost(30) }),
      row({ key: UNATTRIBUTED_TURN_KEY, ordinal: null, cost: cost(1000) }),
    ]
    const trend = halfCostTrend(rows)
    expect(trend).not.toBeNull()
    expect(trend?.firstHalfCost).toBe(30)
    expect(trend?.secondHalfCost).toBe(30)
    expect(trend?.pivot.key).toBe('c')
    expect(trend?.changeFraction).toBeCloseTo(0)
  })

  it('leaves changeFraction null when the first half has no cost to compare against', () => {
    const rows = [row({ key: 'a', ordinal: 1, cost: null }), row({ key: 'b', ordinal: 2, cost: cost(5) })]
    expect(halfCostTrend(rows)?.changeFraction).toBeNull()
  })
})

describe('unattributedCostShare', () => {
  it('is null when there is no unattributed row', () => {
    expect(unattributedCostShare([row({ key: 'a' })])).toBeNull()
  })

  it('is null when the unattributed row carries no cost', () => {
    expect(unattributedCostShare([row({ key: UNATTRIBUTED_TURN_KEY, cost: null })])).toBeNull()
  })

  it('shares against turn cost plus its own, matching costConcentration\'s denominator', () => {
    const rows = [row({ key: 'a', cost: cost(90) }), row({ key: UNATTRIBUTED_TURN_KEY, cost: cost(10) })]
    const result = unattributedCostShare(rows)
    expect(result?.cost).toBe(10)
    expect(result?.share).toBeCloseTo(0.1)
  })
})
