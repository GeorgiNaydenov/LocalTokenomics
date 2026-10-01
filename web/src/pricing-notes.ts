import type { CostBreakdown, CostState } from './api'
import { formatMoney } from './format'

export const ESTIMATED_HELP =
  "Priced from a sibling model's rate because this model has no rate row of its own."

export const EXPERIMENTAL_HELP =
  "Built from the tool's documented log format and test fixtures; not yet confirmed against a real session. Totals may be off: compare with the tool's own display."

export const REPORTED_DIVERGENCE_NOTE =
  "Our figure uses rates.json prices; the tool's own price list differs."

export const CACHE_READ_RATIO_COPY =
  'Cache reads bill at a fraction of the input price (the exact ratio is per model: see Pricing).'

export const STALE_INFO_DAYS = 30
export const STALE_CAUTION_DAYS = 90

export type StaleSeverity = 'info' | 'caution'

export interface RatesAgeNotice {
  severity: StaleSeverity
  text: string
}

/** Staleness notice for the rate table: null under 30 days or when the age is unknown. */
export function ratesAgeNotice(days: number | null | undefined): RatesAgeNotice | null {
  if (days === null || days === undefined || !Number.isFinite(days)) return null
  if (days < STALE_INFO_DAYS) return null
  return {
    severity: days >= STALE_CAUTION_DAYS ? 'caution' : 'info',
    text: `Prices are ${Math.floor(days)} days old: they may have moved. See Pricing.`,
  }
}

/** True when the tool's own figure differs from ours by more than max(5%, $0.01). */
export function reportedDiverges(computed: number, reported: number): boolean {
  return Math.abs(computed - reported) > Math.max(0.05 * Math.abs(computed), 0.01)
}

export interface ReportedNote {
  line: string
  diverges: boolean
  note: string | null
}

/** Secondary "Reported by tool" line for a computed cost; null when the tool wrote none. */
export function reportedNote(computed: number | null, reported: number | null): ReportedNote | null {
  if (reported === null || reported === undefined) return null
  const diverges = computed !== null && reportedDiverges(computed, reported)
  return {
    line: `Reported by tool: ${formatMoney(reported)}`,
    diverges,
    note: diverges ? REPORTED_DIVERGENCE_NOTE : null,
  }
}

/** Tooltip text for a cost cell: reported line plus the divergence note when it applies. */
export function reportedTitle(computed: number | null, reported: number | null): string | null {
  const info = reportedNote(computed, reported)
  if (!info) return null
  return info.note ? `${info.line}. ${info.note}` : info.line
}

/** A priced row whose rate was estimated from a sibling model. */
export function isEstimatedPriced(state: CostState, cost: Pick<CostBreakdown, 'estimated'> | null): boolean {
  return state === 'priced' && cost !== null && cost.estimated === true
}
