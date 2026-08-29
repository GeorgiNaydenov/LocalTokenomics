import { Bar, BarChart, Cell, LabelList, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import type { TooltipContentProps } from 'recharts'
import type { Bucket } from '../api'
import { formatCount, formatExact, formatMoney, formatTokens } from '../format'
import type { ThemeMode } from '../theme'
import { chartInk, seriesColor } from '../theme'
import { ChartEmpty, TooltipShell } from './ChartKit'

interface CostByModelProps {
  buckets: Bucket[]
  identityIndex: (key: string) => number
  mode: ThemeMode
}

const ROW = 34

export function CostByModel({ buckets, identityIndex, mode }: CostByModelProps) {
  const ink = chartInk(mode)
  const rows = [...buckets].sort((a, b) => b.cost.total - a.cost.total)
  const height = Math.max(rows.length * ROW + 16, 120)

  if (rows.length === 0) return <ChartEmpty height={200} message="No models in this slice." />

  return (
    <div style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={rows}
          layout="vertical"
          margin={{ top: 0, right: 68, bottom: 0, left: 0 }}
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
              const bucket = props.payload?.[0]?.payload as Bucket | undefined
              if (!props.active || !bucket) return null
              const color = seriesColor(identityIndex(bucket.key), mode)
              return (
                <TooltipShell
                  title={bucket.label}
                  rows={[
                    { color, label: 'Cost', value: formatMoney(bucket.cost.total) },
                    {
                      color: 'transparent',
                      label: 'Tokens',
                      value: formatTokens(bucket.tokens.total),
                      title: formatExact(bucket.tokens.total),
                    },
                    {
                      color: 'transparent',
                      label: 'Requests',
                      value: formatCount(bucket.events),
                    },
                  ]}
                  footer={
                    <span className="flex justify-between">
                      <span>Saved by caching</span>
                      <span className="tnum font-medium text-ink">
                        {formatMoney(bucket.cost.cache_savings)}
                      </span>
                    </span>
                  }
                />
              )
            }}
          />
          <Bar
            dataKey="cost.total"
            maxBarSize={22}
            radius={[0, 4, 4, 0]}
            isAnimationActive={false}
          >
            {rows.map((bucket) => (
              <Cell key={bucket.key} fill={seriesColor(identityIndex(bucket.key), mode)} />
            ))}
            <LabelList
              dataKey="cost.total"
              position="right"
              offset={8}
              formatter={(value: unknown) => formatMoney(Number(value))}
              style={{ fill: ink.ink, fontSize: 12, fontVariantNumeric: 'tabular-nums' }}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
