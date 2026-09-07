import { useMemo } from 'react'
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { TooltipContentProps } from 'recharts'
import type { SeriesPoint } from '../api'
import {
  daySpan,
  formatDay,
  formatDayShort,
  formatExact,
  formatMoney,
  formatMoneyShort,
  formatTokens,
} from '../format'
import type { ThemeMode } from '../theme'
import { chartInk, seriesColor } from '../theme'
import { ChartEmpty, ChartLegend, TooltipShell } from './ChartKit'

export type StackBy = 'client' | 'provider' | 'model'
export type Metric = 'cost' | 'tokens'

interface CostOverTimeProps {
  series: SeriesPoint[]
  stackBy: StackBy
  metric: Metric
  identityIndex: (dimension: StackBy, key: string) => number
  labelFor: (dimension: StackBy, key: string) => string
  mode: ThemeMode
  height?: number
}

export function CostOverTime({
  series,
  stackBy,
  metric,
  identityIndex,
  labelFor,
  mode,
  height = 300,
}: CostOverTimeProps) {
  const ink = chartInk(mode)

  const { rows, keys } = useMemo(() => {
    if (series.length === 0) return { rows: [], keys: [] as string[] }
    let first = series[0].day
    let last = series[0].day
    const totals = new Map<string, number>()
    for (const point of series) {
      if (point.day < first) first = point.day
      if (point.day > last) last = point.day
      const value = metric === 'cost' ? point.cost : point.tokens
      totals.set(point[stackBy], (totals.get(point[stackBy]) ?? 0) + value)
    }
    const byDay = new Map<string, Record<string, number>>()
    for (const day of daySpan(first, last)) byDay.set(day, { day: 0 })
    for (const point of series) {
      const row = byDay.get(point.day)
      if (!row) continue
      const value = metric === 'cost' ? point.cost : point.tokens
      row[point[stackBy]] = (row[point[stackBy]] ?? 0) + value
    }
    const orderedKeys = [...totals.entries()]
      .filter(([, value]) => value > 0)
      .map(([key]) => key)
      .sort((a, b) => identityIndex(stackBy, a) - identityIndex(stackBy, b))
    const built = [...byDay.entries()].map(([day, values]) => {
      const row: Record<string, string | number> = { day }
      for (const key of orderedKeys) row[key] = values[key] ?? 0
      return row
    })
    return { rows: built, keys: orderedKeys }
  }, [series, stackBy, metric, identityIndex])

  const colorOf = (key: string) => seriesColor(identityIndex(stackBy, key), mode)
  const fmt = metric === 'cost' ? formatMoney : formatTokens

  if (rows.length === 0) {
    return <ChartEmpty height={height} message="No usage in this range." />
  }

  const asColumns = rows.length <= 2

  const grid = <CartesianGrid stroke={ink.grid} strokeWidth={1} vertical={false} />
  const xAxis = (
    <XAxis
      dataKey="day"
      tickFormatter={(value: string) => formatDayShort(value)}
      tickLine={false}
      axisLine={{ stroke: ink.axis }}
      minTickGap={36}
      tick={{ fontSize: 11.5, fill: ink.muted }}
      tickMargin={8}
    />
  )
  const yAxis = (
    <YAxis
      width={58}
      tickFormatter={(value: number) =>
        metric === 'cost' ? formatMoneyShort(value) : formatTokens(value)
      }
      tickLine={false}
      axisLine={false}
      tick={{ fontSize: 11.5, fill: ink.muted }}
    />
  )
  const tooltip = (
    <Tooltip
      cursor={
        asColumns
          ? { fill: ink.grid, fillOpacity: 0.5 }
          : { stroke: ink.axis, strokeWidth: 1 }
      }
      isAnimationActive={false}
      content={(props: TooltipContentProps) => {
        const payload = props.payload ?? []
        if (!props.active || payload.length === 0) return null
        const entries = payload
          .map((item) => ({
            key: String(item.dataKey ?? item.name ?? ''),
            value: typeof item.value === 'number' ? item.value : 0,
          }))
          .filter((item) => item.value > 0)
          .sort((a, b) => b.value - a.value)
        if (entries.length === 0) return null
        const total = entries.reduce((sum, item) => sum + item.value, 0)
        return (
          <TooltipShell
            title={formatDay(String(props.label))}
            rows={entries.map((item) => ({
              color: colorOf(item.key),
              label: labelFor(stackBy, item.key),
              value: fmt(item.value),
              title: metric === 'tokens' ? formatExact(item.value) : undefined,
            }))}
            footer={
              <span className="flex justify-between">
                <span>Total</span>
                <span className="tnum font-medium text-ink">{fmt(total)}</span>
              </span>
            }
          />
        )
      }}
    />
  )

  const margin = { top: 4, right: 8, bottom: 0, left: 0 }

  return (
    <>
      <ChartLegend
        items={keys.map((key) => ({
          key,
          label: labelFor(stackBy, key),
          color: colorOf(key),
        }))}
      />
      <div style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          {asColumns ? (
            <BarChart data={rows} margin={margin}>
              {grid}
              {xAxis}
              {yAxis}
              {tooltip}
              {keys.map((key) => (
                <Bar
                  key={key}
                  dataKey={key}
                  stackId="stack"
                  fill={colorOf(key)}
                  stroke={ink.surface}
                  strokeWidth={2}
                  maxBarSize={72}
                  isAnimationActive={false}
                />
              ))}
            </BarChart>
          ) : (
            <AreaChart data={rows} margin={margin}>
              {grid}
              {xAxis}
              {yAxis}
              {tooltip}
              {keys.map((key) => (
                <Area
                  key={key}
                  type="linear"
                  dataKey={key}
                  stackId="stack"
                  stroke={colorOf(key)}
                  strokeWidth={1.5}
                  fill={colorOf(key)}
                  fillOpacity={0.85}
                  isAnimationActive={false}
                  activeDot={false}
                />
              ))}
            </AreaChart>
          )}
        </ResponsiveContainer>
      </div>
    </>
  )
}
