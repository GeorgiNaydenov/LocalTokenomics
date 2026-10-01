import type {
  ModelRate,
  PriceSet,
  ProviderRules,
  RateBand,
  RatePeak,
  RatePeriod,
  RateTable,
  UnpricedModelEntry,
} from './api'
import { formatCount } from './format'

const PROVIDER_LABELS: Record<string, string> = {
  openai: 'OpenAI',
  xai: 'xAI',
  deepseek: 'DeepSeek',
  moonshot: 'Moonshot',
  alibaba: 'Alibaba',
  zhipu: 'Zhipu',
  mistral: 'Mistral',
  minimax: 'MiniMax',
  amazon: 'Amazon',
  anthropic: 'Anthropic',
  google: 'Google',
  meta: 'Meta',
  typesafe: 'TypeSafe AI',
  bedrock: 'Bedrock',
  openrouter: 'OpenRouter',
  azure: 'Azure',
  'github-copilot': 'GitHub Copilot',
  local: 'Local',
}

export function providerLabel(id: string): string {
  return PROVIDER_LABELS[id] ?? id.charAt(0).toUpperCase() + id.slice(1)
}

/** `1M`, `272K`, `1.05M`. Null when the window is unknown. */
export function formatContextWindow(tokens: number | null): string | null {
  if (tokens === null || tokens <= 0) return null
  const trim = (value: number) => String(Number(value.toFixed(2)))
  if (tokens >= 1_000_000) return `${trim(tokens / 1_000_000)}M`
  if (tokens >= 1000) return `${trim(tokens / 1000)}K`
  return String(tokens)
}

/** Provider block with the row's `cache_rules` laid over it field by field. Null when the
 * provider has no block: nothing is invented in that case. */
export function mergedRules(rate: ModelRate, rates: RateTable): ProviderRules | null {
  const base = rates.providers[rate.provider]
  if (!base) return null
  const over = rate.cache_rules
  if (!over) return base
  return {
    cache_read: over.cache_read ?? base.cache_read,
    cache_write_5m: over.cache_write_5m ?? base.cache_write_5m,
    cache_write_1h: over.cache_write_1h ?? base.cache_write_1h,
    batch: over.batch ?? base.batch,
    free: over.free ?? base.free,
  }
}

export type CacheField = 'cache_read' | 'cache_write_5m' | 'cache_write_1h'

/** Cache price for a row: the published absolute figure, else input times the merged ratio,
 * else null (no provider block, so nothing to derive from). */
export function cachePrice(rate: ModelRate, rules: ProviderRules | null, field: CacheField): number | null {
  const absolute = rate[field]
  if (absolute !== null) return absolute
  if (!rules) return null
  return rate.input * rules[field]
}

export function usd(value: number, digits = 2): string {
  return `$${value.toFixed(digits)}`
}

function cachePart(label: string, value: number | null): string | null {
  return value === null ? null : `${label} ${usd(value, 3)}`
}

/** `$3.00 in / $15.00 out, cache read $0.300 ...` (cache only when published). */
export function priceText(price: PriceSet): string {
  const cache = [
    cachePart('cache read', price.cache_read),
    cachePart('write 5m', price.cache_write_5m),
    cachePart('write 1h', price.cache_write_1h),
  ].filter((part): part is string => part !== null)
  return [`${usd(price.input)} in / ${usd(price.output)} out`, ...cache].join(', ')
}

export function bandText(band: RateBand): string {
  return `from ${formatCount(band.min_input_tokens)} input tokens: ${priceText(band)}`
}

const WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

function weekdayText(days: number[]): string {
  const sorted = [...new Set(days)].filter((d) => d >= 0 && d <= 6).sort((a, b) => a - b)
  const runs: string[] = []
  let i = 0
  while (i < sorted.length) {
    let j = i
    while (j + 1 < sorted.length && sorted[j + 1] === sorted[j] + 1) j += 1
    runs.push(j > i ? `${WEEKDAYS[sorted[i]]}-${WEEKDAYS[sorted[j]]}` : WEEKDAYS[sorted[i]])
    i = j + 1
  }
  return runs.join(', ')
}

function hour(h: number): string {
  return `${String(h).padStart(2, '0')}:00`
}

/** `Mon-Fri 01:00-04:00, 06:00-10:00 UTC`. */
export function peakWindowText(peak: RatePeak): string {
  const hours = peak.utc_hours.map(([start, end]) => `${hour(start)}-${hour(end)}`).join(', ')
  return `${weekdayText(peak.weekdays)} ${hours} UTC`
}

export function peakText(peak: RatePeak): string {
  return `${peakWindowText(peak)}: ${priceText(peak)}`
}

export function periodRangeText(period: RatePeriod): string {
  if (period.from && period.until) return `${period.from} to ${period.until}`
  if (period.from) return `from ${period.from}`
  if (period.until) return `until ${period.until}`
  return 'always'
}

/** The price in force during a period. A null input/output keeps the row's own figure. */
export function periodText(period: RatePeriod, rate: ModelRate): string {
  return `${periodRangeText(period)}: ${priceText({
    input: period.input ?? rate.input,
    output: period.output ?? rate.output,
    cache_read: period.cache_read,
    cache_write_5m: period.cache_write_5m,
    cache_write_1h: period.cache_write_1h,
  })}`
}

export interface RateTag {
  key: 'preview' | 'retired' | 'unverified'
  label: string
  hint: string | null
}

export function rateTags(rate: ModelRate): RateTag[] {
  const tags: RateTag[] = []
  if (rate.status === 'preview') tags.push({ key: 'preview', label: 'Preview', hint: null })
  if (rate.status === 'retired') tags.push({ key: 'retired', label: 'Retired', hint: null })
  if (rate.verified === null) {
    tags.push({
      key: 'unverified',
      label: 'Unverified',
      hint: 'No vendor page could be read for this price',
    })
  }
  return tags
}

export type Staleness = { level: 'info' | 'caution'; text: string }

export function stalenessBadge(days: number | null): Staleness | null {
  if (days === null) return null
  if (days >= 90) return { level: 'caution', text: '90+ days old; prices may have moved' }
  if (days >= 30) return { level: 'info', text: '30+ days old' }
  return null
}

/** Longest-prefix match of a model id against the no-list-price entries (case-insensitive). */
export function matchUnpriced(model: string, entries: UnpricedModelEntry[]): UnpricedModelEntry | null {
  const id = model.toLowerCase()
  let best: UnpricedModelEntry | null = null
  for (const entry of entries) {
    const prefix = entry.match.toLowerCase()
    if (id.startsWith(prefix) && (best === null || prefix.length > best.match.length)) best = entry
  }
  return best
}
