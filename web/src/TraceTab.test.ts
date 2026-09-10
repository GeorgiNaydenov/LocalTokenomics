import { describe, expect, it } from 'vitest'
import type { Insight, Span, TokenUsage } from './api'
import { groupSpansByTurn, resolveInsightTurn, spanWindow, summarizeInsightTurns } from './TraceTab'

function span(overrides: Partial<Span> = {}): Span {
  return {
    span_id: 'span',
    parent_id: null,
    turn_id: null,
    kind: 'model_call',
    seq: 0,
    started_at: '2026-01-01T00:00:00Z',
    ended_at: null,
    duration_ms: null,
    ...overrides,
  } as unknown as Span
}

function turnFixture(overrides: Partial<Span> = {}): Span {
  return {
    span_id: 'span',
    parent_id: null,
    turn_id: null,
    kind: 'model_call',
    seq: 0,
    status: 'ok',
    started_at: '2026-01-01T00:00:00Z',
    ended_at: null,
    duration_ms: null,
    duration_provenance: 'unavailable',
    tokens: null,
    tokens_provenance: 'unavailable',
    is_sidechain: false,
    model: null,
    ...overrides,
  } as unknown as Span
}

function tokenUsage(inputTotal: number, output: number): TokenUsage {
  return {
    uncached_input: inputTotal,
    cache_read: 0,
    cache_write_5m: 0,
    cache_write_1h: 0,
    output,
    reasoning_output: 0,
    cache_write: 0,
    input_total: inputTotal,
    total: inputTotal + output,
  }
}

function insight(overrides: Partial<Insight> = {}): Insight {
  return {
    kind: 'amplification',
    severity: 'warning',
    span_id: 'span',
    message: 'message',
    count: 1,
    ...overrides,
  }
}

describe('spanWindow', () => {
  it('uses the logged end time when present', () => {
    const window = spanWindow(span({ started_at: '2026-01-01T00:00:00Z', ended_at: '2026-01-01T00:00:05Z' }))
    expect(window.start).toBe(Date.parse('2026-01-01T00:00:00Z'))
    expect(window.end).toBe(Date.parse('2026-01-01T00:00:05Z'))
  })

  it('derives the end from start plus duration when no end time is logged', () => {
    const window = spanWindow(span({ started_at: '2026-01-01T00:00:00Z', duration_ms: 5000 }))
    expect(window.end).toBe(Date.parse('2026-01-01T00:00:00Z') + 5000)
  })

  it('leaves the end unknown when neither an end time nor a duration is logged', () => {
    const window = spanWindow(span({ started_at: '2026-01-01T00:00:00Z' }))
    expect(window.end).toBeNull()
  })

  it('leaves the start unknown for an unparsable timestamp', () => {
    const window = spanWindow(span({ started_at: 'not a date' }))
    expect(window.start).toBeNull()
  })
})

describe('resolveInsightTurn', () => {
  it('uses the span own turn_id directly when set', () => {
    const spans = [
      span({ span_id: 'turn-1', kind: 'turn', seq: 0 }),
      span({ span_id: 'call-1', kind: 'model_call', turn_id: 'turn-1', seq: 1 }),
    ]
    const turn = resolveInsightTurn('call-1', spans)
    expect(turn).toEqual({ key: 'turn-1', spanId: 'turn-1', label: 'Turn 1' })
  })

  it('walks the parent_id chain to find an ancestor turn span', () => {
    const spans = [
      span({ span_id: 'turn-1', kind: 'turn', seq: 0 }),
      span({ span_id: 'assistant-1', kind: 'assistant', parent_id: 'turn-1', seq: 1 }),
      span({ span_id: 'call-1', kind: 'model_call', parent_id: 'assistant-1', seq: 2 }),
    ]
    const turn = resolveInsightTurn('call-1', spans)
    expect(turn).toEqual({ key: 'turn-1', spanId: 'turn-1', label: 'Turn 1' })
  })

  it('numbers turns in seq order across multiple turns', () => {
    const spans = [
      span({ span_id: 'turn-1', kind: 'turn', seq: 0 }),
      span({ span_id: 'turn-2', kind: 'turn', seq: 10 }),
      span({ span_id: 'call-1', kind: 'model_call', turn_id: 'turn-2', seq: 11 }),
    ]
    const turn = resolveInsightTurn('call-1', spans)
    expect(turn?.label).toBe('Turn 2')
  })

  it('returns null when the span has no resolvable turn', () => {
    const spans = [
      span({ span_id: 'orphan-1', kind: 'model_call', seq: 0 }),
      span({ span_id: 'orphan-2', kind: 'tool_call', parent_id: 'orphan-1', seq: 1 }),
    ]
    const turn = resolveInsightTurn('orphan-2', spans)
    expect(turn).toBeNull()
  })

  it('returns null for an unknown span id', () => {
    expect(resolveInsightTurn('missing', [])).toBeNull()
  })

  it('stops at the depth cap instead of looping on a cyclical parent chain', () => {
    const spans = [
      span({ span_id: 'a', kind: 'model_call', parent_id: 'b', seq: 0 }),
      span({ span_id: 'b', kind: 'model_call', parent_id: 'a', seq: 1 }),
    ]
    expect(resolveInsightTurn('a', spans)).toBeNull()
  })
})

describe('summarizeInsightTurns', () => {
  it('returns null when the session has no turns at all', () => {
    expect(summarizeInsightTurns([insight()], [])).toBeNull()
  })

  it('reports every turn carrying an insight when spread evenly', () => {
    const spans = [
      span({ span_id: 'turn-1', kind: 'turn', seq: 0 }),
      span({ span_id: 'turn-2', kind: 'turn', seq: 1 }),
      span({ span_id: 'turn-3', kind: 'turn', seq: 2 }),
      span({ span_id: 'turn-4', kind: 'turn', seq: 3 }),
    ]
    const insights = [
      insight({ kind: 'amplification', span_id: 'turn-1', count: 1 }),
      insight({ kind: 'cache_miss', span_id: 'turn-2', count: 1 }),
      insight({ kind: 'model_switch', span_id: 'turn-3', count: 1 }),
      insight({ kind: 'context_pressure', span_id: 'turn-4', count: 1 }),
    ]
    const summary = summarizeInsightTurns(insights, spans)
    expect(summary).toBe('4 of 4 turns carry at least one insight.')
  })

  it('names the dominant turns once they pass half the weighted total', () => {
    const spans = [
      span({ span_id: 'turn-1', kind: 'turn', seq: 0 }),
      span({ span_id: 'turn-2', kind: 'turn', seq: 1 }),
    ]
    const insights = [
      insight({ kind: 'amplification', span_id: 'turn-1', count: 9 }),
      insight({ kind: 'cache_miss', span_id: 'turn-2', count: 1 }),
    ]
    const summary = summarizeInsightTurns(insights, spans)
    expect(summary).toBe('2 of 2 turns carry at least one insight. Turn 1 accounts for 90% of them.')
  })

  it('stays under the threshold when the top turns hold half or less', () => {
    const spans = [
      span({ span_id: 'turn-1', kind: 'turn', seq: 0 }),
      span({ span_id: 'turn-2', kind: 'turn', seq: 1 }),
    ]
    const insights = [
      insight({ kind: 'amplification', span_id: 'turn-1', count: 1 }),
      insight({ kind: 'cache_miss', span_id: 'turn-2', count: 1 }),
    ]
    const summary = summarizeInsightTurns(insights, spans)
    expect(summary).toBe('2 of 2 turns carry at least one insight.')
  })

  it('says nothing could be tied to a turn when every insight is unresolvable', () => {
    const spans = [span({ span_id: 'turn-1', kind: 'turn', seq: 0 })]
    const insights = [insight({ kind: 'amplification', span_id: 'orphan', count: 1 })]
    const summary = summarizeInsightTurns(insights, spans)
    expect(summary).toBe("None of this session's insights could be tied to a turn, out of 1 turn total.")
  })
})

describe('groupSpansByTurn', () => {
  it('groups spans under the turn span sharing their turn_id, excluding it from the breakdown', () => {
    const spans = [
      turnFixture({ span_id: 'turn-1', turn_id: 'turn-1', kind: 'turn', seq: 0 }),
      turnFixture({ span_id: 'call-1', turn_id: 'turn-1', kind: 'model_call', seq: 1 }),
      turnFixture({ span_id: 'tool-1', turn_id: 'turn-1', kind: 'tool_call', seq: 2 }),
    ]
    const rollups = groupSpansByTurn(spans)
    expect(rollups).toHaveLength(1)
    expect(rollups[0].turnId).toBe('turn-1')
    expect(rollups[0].spanCount).toBe(3)
    expect(rollups[0].kindCounts).toEqual([
      ['model_call', 1],
      ['tool_call', 1],
    ])
  })

  it('orders turns chronologically by the turn span started_at', () => {
    const spans = [
      turnFixture({ span_id: 'turn-2', turn_id: 'turn-2', kind: 'turn', seq: 10, started_at: '2026-01-01T00:05:00Z' }),
      turnFixture({ span_id: 'turn-1', turn_id: 'turn-1', kind: 'turn', seq: 0, started_at: '2026-01-01T00:00:00Z' }),
    ]
    const rollups = groupSpansByTurn(spans)
    expect(rollups.map((rollup) => rollup.turnId)).toEqual(['turn-1', 'turn-2'])
    expect(rollups.map((rollup) => rollup.ordinal)).toEqual([1, 2])
  })

  it('falls back to the earliest child span start when the turn span itself is missing', () => {
    const spans = [
      turnFixture({ span_id: 'call-2', turn_id: 'turn-1', kind: 'model_call', seq: 1, started_at: '2026-01-01T00:02:00Z' }),
      turnFixture({ span_id: 'call-1', turn_id: 'turn-1', kind: 'model_call', seq: 0, started_at: '2026-01-01T00:01:00Z' }),
    ]
    const rollups = groupSpansByTurn(spans)
    expect(rollups[0].span).toBeNull()
    expect(rollups[0].startedAt).toBe('2026-01-01T00:01:00Z')
  })

  it("uses the turn span's own duration directly and never sums children", () => {
    const spans = [
      turnFixture({
        span_id: 'turn-1',
        turn_id: 'turn-1',
        kind: 'turn',
        seq: 0,
        duration_ms: 500,
        duration_provenance: 'measured',
      }),
      turnFixture({
        span_id: 'call-1',
        turn_id: 'turn-1',
        kind: 'model_call',
        seq: 1,
        duration_ms: 400,
        duration_provenance: 'measured',
      }),
      turnFixture({
        span_id: 'call-2',
        turn_id: 'turn-1',
        kind: 'model_call',
        seq: 2,
        duration_ms: 400,
        duration_provenance: 'measured',
      }),
    ]
    const rollups = groupSpansByTurn(spans)
    expect(rollups[0].duration).toBe(500)
    expect(rollups[0].durationProvenance).toBe('measured')
  })

  it('marks duration unavailable when the turn span carries none, even though children do', () => {
    const spans = [
      turnFixture({ span_id: 'turn-1', turn_id: 'turn-1', kind: 'turn', seq: 0 }),
      turnFixture({
        span_id: 'call-1',
        turn_id: 'turn-1',
        kind: 'model_call',
        seq: 1,
        duration_ms: 400,
        duration_provenance: 'measured',
      }),
    ]
    const rollups = groupSpansByTurn(spans)
    expect(rollups[0].duration).toBeNull()
    expect(rollups[0].durationProvenance).toBe('unavailable')
  })

  it("sums input and output tokens across the turn's model_call spans", () => {
    const spans = [
      turnFixture({ span_id: 'turn-1', turn_id: 'turn-1', kind: 'turn', seq: 0 }),
      turnFixture({
        span_id: 'call-1',
        turn_id: 'turn-1',
        kind: 'model_call',
        seq: 1,
        tokens: tokenUsage(100, 20),
        tokens_provenance: 'measured',
      }),
      turnFixture({
        span_id: 'call-2',
        turn_id: 'turn-1',
        kind: 'model_call',
        seq: 2,
        tokens: tokenUsage(50, 10),
        tokens_provenance: 'measured',
      }),
    ]
    const rollups = groupSpansByTurn(spans)
    expect(rollups[0].tokens).toEqual({ inputTotal: 150, output: 30 })
    expect(rollups[0].tokensProvenance).toBe('measured')
  })

  it('marks tokens unavailable when any contributing model_call span has none, rather than treating it as zero', () => {
    const spans = [
      turnFixture({ span_id: 'turn-1', turn_id: 'turn-1', kind: 'turn', seq: 0 }),
      turnFixture({
        span_id: 'call-1',
        turn_id: 'turn-1',
        kind: 'model_call',
        seq: 1,
        tokens: tokenUsage(100, 20),
        tokens_provenance: 'measured',
      }),
      turnFixture({ span_id: 'call-2', turn_id: 'turn-1', kind: 'model_call', seq: 2 }),
    ]
    const rollups = groupSpansByTurn(spans)
    expect(rollups[0].tokens).toBeNull()
    expect(rollups[0].tokensProvenance).toBe('unavailable')
  })

  it('collects spans with no turn_id into an "Outside any turn" group placed last', () => {
    const spans = [
      turnFixture({ span_id: 'turn-1', turn_id: 'turn-1', kind: 'turn', seq: 0, started_at: '2026-01-01T00:10:00Z' }),
      turnFixture({ span_id: 'stray-1', turn_id: null, kind: 'model_call', seq: 1, started_at: '2026-01-01T00:00:00Z' }),
    ]
    const rollups = groupSpansByTurn(spans)
    expect(rollups).toHaveLength(2)
    expect(rollups[1].turnId).toBeNull()
    expect(rollups[1].label).toBe('Outside any turn')
    expect(rollups[1].spanCount).toBe(1)
    expect(rollups[1].ordinal).toBe(2)
  })

  it('counts a failed tool call once, not twice for the call and its paired result', () => {
    const spans = [
      turnFixture({ span_id: 'turn-1', turn_id: 'turn-1', kind: 'turn', seq: 0 }),
      turnFixture({ span_id: 'call-1', turn_id: 'turn-1', kind: 'tool_call', seq: 1, status: 'error' }),
      turnFixture({
        span_id: 'result-1',
        turn_id: 'turn-1',
        kind: 'tool_result',
        parent_id: 'call-1',
        seq: 2,
        status: 'error',
      }),
    ]
    const rollups = groupSpansByTurn(spans)
    expect(rollups[0].errorCount).toBe(1)
  })

  it('still counts a failed tool call with no paired result', () => {
    const spans = [
      turnFixture({ span_id: 'turn-1', turn_id: 'turn-1', kind: 'turn', seq: 0 }),
      turnFixture({ span_id: 'call-1', turn_id: 'turn-1', kind: 'tool_call', seq: 1, status: 'error' }),
    ]
    const rollups = groupSpansByTurn(spans)
    expect(rollups[0].errorCount).toBe(1)
  })

  it("collects the distinct models used by the turn's model_call spans", () => {
    const spans = [
      turnFixture({ span_id: 'turn-1', turn_id: 'turn-1', kind: 'turn', seq: 0 }),
      turnFixture({ span_id: 'call-1', turn_id: 'turn-1', kind: 'model_call', seq: 1, model: 'claude-opus' }),
      turnFixture({ span_id: 'call-2', turn_id: 'turn-1', kind: 'model_call', seq: 2, model: 'claude-opus' }),
      turnFixture({ span_id: 'call-3', turn_id: 'turn-1', kind: 'model_call', seq: 3, model: 'claude-haiku' }),
    ]
    const rollups = groupSpansByTurn(spans)
    expect(rollups[0].models).toEqual(['claude-opus', 'claude-haiku'])
  })

  it('reads is_sidechain from the turn span', () => {
    const spans = [turnFixture({ span_id: 'turn-1', turn_id: 'turn-1', kind: 'turn', seq: 0, is_sidechain: true })]
    const rollups = groupSpansByTurn(spans)
    expect(rollups[0].isSidechain).toBe(true)
  })

  it('returns nothing for an empty trace', () => {
    expect(groupSpansByTurn([])).toEqual([])
  })
})
