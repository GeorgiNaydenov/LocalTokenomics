import {
  Bar,
  BarChart,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { TooltipContentProps } from 'recharts'
import type { Bucket } from '../api'
import { formatExact, formatPercent, formatTokens } from '../format'
import type { ThemeMode } from '../theme'
import { TOKEN_PARTS, chartInk, seriesColor } from '../theme'
import { ChartEmpty, ChartLegend, TooltipShell } from './ChartKit'

interface TokenMixProps {
  buckets: Bucket[]
  mode: ThemeMode
}

interface MixRow {
  key: string
  label: string
  total: number
  uncached_input: number
  cache_read: number
  cache_write: number
  output: number
}

const ROW = 34

/**
 * The four parts sum exactly to `tokens.total`, so this is a true part-to-whole.
 * A 2px surface-coloured stroke is the gap between segments, not a border.
 */
export function TokenMix({ buckets, mode }: TokenMixProps) {
  const ink = chartInk(mode)
  const rows: MixRow[] = [...buckets]
    .sort((a, b) => b.tokens.total - a.tokens.total)
    .map((bucket) => ({
      key: bucket.key,
      label: bucket.label,
      total: bucket.tokens.total,
      uncached_input: bucket.tokens.uncached_input,
      cache_read: bucket.tokens.cache_read,
      cache_write: bucket.tokens.cache_write,
      output: bucket.tokens.output,
    }))
  const height = Math.max(rows.length * ROW + 16, 120)

  if (rows.length === 0) return <ChartEmpty height={200} message="No models in this slice." />

  return (
    <>
      <ChartLegend
        items={TOKEN_PARTS.map((part) => ({
          key: part.key,
          label: part.label,
          color: seriesColor(part.slot, mode),
        }))}
      />
      <div style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={rows}
            layout="vertical"
            margin={{ top: 0, right: 62, bottom: 0, left: 0 }}
            barCategoryGap="28%"
          >
            <XAxis type="number" hide />
            <YAxis
              type="category"
              dataKey="label"
              width={152}
              tickLine={false}
              axisLine={false}
              tick={{ fontSize: 12, fill: ink.ink2 }}
              interval={0}
            />
            <Tooltip
              cursor={{ fill: ink.grid, fillOpacity: 0.5 }}
              isAnimationActive={false}
              content={(props: TooltipContentProps) => {
                const row = props.payload?.[0]?.payload as MixRow | undefined
                if (!props.active || !row) return null
                return (
                  <TooltipShell
                    title={row.label}
                    rows={TOKEN_PARTS.map((part) => ({
                      color: seriesColor(part.slot, mode),
                      label: part.label,
                      value: `${formatTokens(row[part.key])} · ${
                        row.total > 0 ? formatPercent(row[part.key] / row.total) : '0%'
                      }`,
                      title: formatExact(row[part.key]),
                    }))}
                    footer={
                      <span className="flex justify-between">
                        <span>Total</span>
                        <span className="tnum font-medium text-ink" title={formatExact(row.total)}>
                          {formatTokens(row.total)}
                        </span>
                      </span>
                    }
                  />
                )
              }}
            />
            {TOKEN_PARTS.map((part, index) => (
              <Bar
                key={part.key}
                dataKey={part.key}
                stackId="mix"
                fill={seriesColor(part.slot, mode)}
                stroke={ink.surface}
                strokeWidth={2}
                maxBarSize={22}
                isAnimationActive={false}
                radius={index === TOKEN_PARTS.length - 1 ? [0, 4, 4, 0] : undefined}
              >
                {index === TOKEN_PARTS.length - 1 ? (
                  <LabelList
                    dataKey="total"
                    position="right"
                    offset={8}
                    formatter={(value: unknown) => formatTokens(Number(value))}
                    style={{ fill: ink.ink, fontSize: 12, fontVariantNumeric: 'tabular-nums' }}
                  />
                ) : null}
              </Bar>
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </>
  )
}
