export const SERIES_SLOTS = 8

export function seriesColor(index: number): string {
  return index >= 0 && index < SERIES_SLOTS ? `var(--chart-${index + 1})` : 'var(--chart-other)'
}

export interface TokenBucket {
  key: 'uncached_input' | 'cache_read' | 'cache_write' | 'output'
  label: string
  color: string
  multiplier: string
}

export const TOKEN_BUCKETS: TokenBucket[] = [
  {
    key: 'uncached_input',
    label: 'Uncached input',
    color: 'var(--bucket-uncached-input)',
    multiplier: '1x',
  },
  { key: 'cache_read', label: 'Cache read', color: 'var(--bucket-cache-read)', multiplier: '0.1x' },
  {
    key: 'cache_write',
    label: 'Cache write',
    color: 'var(--bucket-cache-write)',
    multiplier: '1.25x',
  },
  { key: 'output', label: 'Output', color: 'var(--bucket-output)', multiplier: 'output rate' },
]
