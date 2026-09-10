import type { EconRow } from './api'

/** Mirrors `UNATTRIBUTED_TURN_KEY` in `src/ai_usage_cost/trace.py`. */
export const UNATTRIBUTED_TURN_KEY = 'unattributed'

/** Mirrors `UNATTRIBUTED_TURN_LABEL` in `src/ai_usage_cost/trace.py`, used only as a
 *  fallback if the row ever arrives without its own label. */
export const UNATTRIBUTED_TURN_LABEL = 'Outside any turn'

/** A share of unattributed cost below this is not worth a line in the strip. */
export const NOTABLE_UNATTRIBUTED_SHARE = 0.02

export type TurnSortKey = 'cost' | 'duration' | 'ordinal' | 'errors'

export function realTurns(rows: EconRow[]): EconRow[] {
  return rows.filter((row) => row.key !== UNATTRIBUTED_TURN_KEY)
}

export function unattributedRow(rows: EconRow[]): EconRow | null {
  return rows.find((row) => row.key === UNATTRIBUTED_TURN_KEY) ?? null
}

/** `<=maxChars` visible characters, an ellipsis appended only when something was cut. */
export function truncateLabel(label: string, maxChars: number): string {
  if (label.length <= maxChars) return label
  return `${label.slice(0, maxChars).trimEnd()}…`
}

/** `Turn 12 · "prompt snippet…"`, `Turn 12` when there is no label, and the
 *  unattributed row's own label when given that row. Never renders an empty
 *  quoted string. */
export function turnLabel(row: EconRow, maxChars = 40): string {
  if (row.key === UNATTRIBUTED_TURN_KEY) return row.label ?? UNATTRIBUTED_TURN_LABEL
  const base = row.ordinal != null ? `Turn ${row.ordinal}` : 'Turn'
  if (!row.label) return base
  return `${base} · "${truncateLabel(row.label, maxChars)}"`
}

function sortValue(row: EconRow, key: TurnSortKey): number {
  switch (key) {
    case 'cost':
      return row.cost?.total ?? -1
    case 'duration':
      return row.duration_ms ?? -1
    case 'ordinal':
      return row.ordinal ?? 0
    case 'errors':
      return row.errors
  }
}

/** Sorts only the real turns; the unattributed row (if present in `rows`) never
 *  takes part, in cost, duration, ordinal or error order alike. */
export function sortRealTurns(rows: EconRow[], key: TurnSortKey, dir: 'asc' | 'desc'): EconRow[] {
  const sorted = realTurns(rows).slice()
  sorted.sort((a, b) => {
    const cmp = sortValue(a, key) - sortValue(b, key)
    return dir === 'desc' ? -cmp : cmp
  })
  return sorted
}

export interface CostConcentration {
  topRows: EconRow[]
  topCost: number
  totalTurnCost: number
  share: number
}

/** Top `topN` turns by cost as a share of the cost carried by turns (not the
 *  session total, which also includes unattributed spans). `null` when no turn
 *  in this session carries a priced cost. */
export function costConcentration(rows: EconRow[], topN = 3): CostConcentration | null {
  const priced = realTurns(rows).filter((row) => row.cost !== null)
  const totalTurnCost = priced.reduce((sum, row) => sum + (row.cost?.total ?? 0), 0)
  if (totalTurnCost <= 0) return null
  const topRows = sortRealTurns(rows, 'cost', 'desc')
    .filter((row) => row.cost !== null)
    .slice(0, topN)
  const topCost = topRows.reduce((sum, row) => sum + (row.cost?.total ?? 0), 0)
  return { topRows, topCost, totalTurnCost, share: topCost / totalTurnCost }
}

export function longestTurn(rows: EconRow[]): EconRow | null {
  const timed = realTurns(rows).filter((row) => row.duration_ms !== null)
  if (timed.length === 0) return null
  return timed.reduce((longest, row) => ((row.duration_ms ?? 0) > (longest.duration_ms ?? 0) ? row : longest))
}

export interface ErrorRetrySummary {
  count: number
  worst: EconRow | null
}

/** Turns with at least one error or one retry: how many, and the single worst
 *  offender, ranked by errors first and retries second. */
export function errorOrRetryTurns(rows: EconRow[]): ErrorRetrySummary {
  const flagged = realTurns(rows).filter((row) => row.errors > 0 || (row.retries ?? 0) > 0)
  if (flagged.length === 0) return { count: 0, worst: null }
  const worst = flagged.reduce((worst, row) => {
    const rowScore = row.errors * 1000 + (row.retries ?? 0)
    const worstScore = worst.errors * 1000 + (worst.retries ?? 0)
    return rowScore > worstScore ? row : worst
  })
  return { count: flagged.length, worst }
}

export function toolHeaviestTurn(rows: EconRow[]): EconRow | null {
  const withTools = realTurns(rows).filter((row) => row.tool_calls > 0)
  if (withTools.length === 0) return null
  return withTools.reduce((most, row) => (row.tool_calls > most.tool_calls ? row : most))
}

export interface HalfTrend {
  firstHalfCost: number
  secondHalfCost: number
  pivot: EconRow
  changeFraction: number | null
}

/** Splits the session's turns, in ordinal order, into two halves by count and
 *  compares their summed cost. `null` when there are fewer than two turns to
 *  split. `pivot` is the first turn of the second half, the natural anchor for
 *  "jump to where the trend starts". `changeFraction` is `null` when the first
 *  half carries no cost to compare against. */
export function halfCostTrend(rows: EconRow[]): HalfTrend | null {
  const ordered = sortRealTurns(rows, 'ordinal', 'asc')
  if (ordered.length < 2) return null
  const mid = Math.ceil(ordered.length / 2)
  const firstHalf = ordered.slice(0, mid)
  const secondHalf = ordered.slice(mid)
  const firstHalfCost = firstHalf.reduce((sum, row) => sum + (row.cost?.total ?? 0), 0)
  const secondHalfCost = secondHalf.reduce((sum, row) => sum + (row.cost?.total ?? 0), 0)
  return {
    firstHalfCost,
    secondHalfCost,
    pivot: secondHalf[0],
    changeFraction: firstHalfCost > 0 ? (secondHalfCost - firstHalfCost) / firstHalfCost : null,
  }
}

export interface UnattributedShare {
  row: EconRow
  cost: number
  share: number
}

/** The unattributed row's cost as a share of turn-attributed cost plus its own,
 *  so it reconciles with `costConcentration`'s denominator. `null` when there
 *  is no unattributed row or it carries no priced cost. */
export function unattributedCostShare(rows: EconRow[]): UnattributedShare | null {
  const row = unattributedRow(rows)
  if (row === null || row.cost === null || row.cost.total <= 0) return null
  const turnCost = realTurns(rows).reduce((sum, turn) => sum + (turn.cost?.total ?? 0), 0)
  const total = turnCost + row.cost.total
  if (total <= 0) return null
  return { row, cost: row.cost.total, share: row.cost.total / total }
}

export function economicsRowDomId(source: string, sessionId: string, key: string): string {
  return `econ-turn-${source}-${sessionId}-${key}`
}
