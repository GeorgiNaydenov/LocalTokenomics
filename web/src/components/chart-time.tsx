import { useMemo } from 'react'
import { Bar, BarChart, CartesianGrid, ReferenceLine, XAxis, YAxis } from 'recharts'

import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from '@/components/ui/chart'
import { seriesColor, SERIES_SLOTS } from '@/components/series'
import { Legend } from '@/components/status'

export interface TimeSeriesRow {
  day: string
  key: string
  label: string
  value: number
}

const LEGEND_LIMIT = SERIES_SLOTS
const OTHER_KEY = '__other__'

export function TimeChart({
  days,
  rows,
  format,
  formatAxis,
  formatDay,
  height = 300,
  className,
}: {
  days: string[]
  rows: TimeSeriesRow[]
  format: (value: number) => string
  formatAxis: (value: number) => string
  formatDay: (day: string) => string
  height?: number
  className?: string
}) {
  const model = useMemo(() => {
    const totals = new Map<string, number>()
    const labels = new Map<string, string>()
    for (const row of rows) {
      totals.set(row.key, (totals.get(row.key) ?? 0) + row.value)
      labels.set(row.key, row.label)
    }
    const keys = [...totals.entries()].sort((a, b) => b[1] - a[1]).map(([key]) => key)

    const byDay = new Map(days.map((day) => [day, Object.create(null) as Record<string, number>]))
    for (const row of rows) {
      const slot = byDay.get(row.day)
      if (!slot) continue
      slot[row.key] = (slot[row.key] ?? 0) + row.value
    }

    const data = days.map((day) => ({ day, ...byDay.get(day) }))
    const dayTotals = days.map((day) =>
      keys.reduce((sum, key) => sum + (byDay.get(day)?.[key] ?? 0), 0),
    )
    const mean = dayTotals.reduce((a, b) => a + b, 0) / Math.max(days.length, 1)
    const peakIndex = dayTotals.indexOf(Math.max(...dayTotals, 0))

    const config: ChartConfig = {}
    keys.forEach((key, index) => {
      config[key] = { label: labels.get(key) ?? key, color: seriesColor(index) }
    })

    const overflowKeys = keys.slice(LEGEND_LIMIT)
    const legend = keys.slice(0, LEGEND_LIMIT).map((key, index) => ({
      key,
      label: labels.get(key) ?? key,
      color: seriesColor(index),
      total: totals.get(key) ?? 0,
    }))
    if (overflowKeys.length > 0) {
      legend.push({
        key: OTHER_KEY,
        label: `Other (${overflowKeys.length})`,
        color: 'var(--chart-other)',
        total: overflowKeys.reduce((sum, key) => sum + (totals.get(key) ?? 0), 0),
      })
    }

    return {
      keys,
      data,
      config,
      mean,
      peakDay: days[peakIndex] ?? null,
      peakValue: dayTotals[peakIndex] ?? 0,
      legend,
    }
  }, [days, rows])

  if (model.keys.length === 0) return null

  return (
    <div className="flex flex-col gap-3">
      <ChartContainer config={model.config} className={className} style={{ height }}>
        <BarChart data={model.data} margin={{ left: 4, right: 12, top: 24 }}>
          <CartesianGrid vertical={false} stroke="var(--chart-grid)" />
          <XAxis
            dataKey="day"
            tickLine={false}
            axisLine={false}
            tickMargin={10}
            minTickGap={28}
            tickFormatter={formatDay}
          />
          <YAxis tickLine={false} axisLine={false} width={56} tickFormatter={formatAxis} />
          <ChartTooltip
            content={
              <ChartTooltipContent
                indicator="dot"
                labelFormatter={(value) => formatDay(String(value))}
                formatter={(value, name, item) => {
                  const indicatorColor = item?.payload?.fill ?? item?.color
                  return (
                    <>
                      <div
                        className="h-2.5 w-2.5 shrink-0 rounded-[2px]"
                        style={{ backgroundColor: indicatorColor }}
                      />
                      <div className="flex flex-1 items-center justify-between gap-2 leading-none">
                        <span className="text-muted-foreground">
                          {model.config[String(name)]?.label ?? name}
                        </span>
                        <span className="tabular font-mono font-medium text-foreground">
                          {format(Number(value))}
                        </span>
                      </div>
                    </>
                  )
                }}
              />
            }
          />
          {model.keys.map((key) => (
            <Bar
              key={key}
              dataKey={key}
              stackId="total"
              fill={model.config[key].color}
              isAnimationActive={false}
            />
          ))}
          <ReferenceLine
            y={model.mean}
            stroke="var(--foreground)"
            strokeDasharray="4 4"
            strokeOpacity={0.55}
            label={{
              value: `mean ${formatAxis(model.mean)} per calendar day`,
              position: 'insideTopLeft',
              fill: 'var(--muted-foreground)',
              fontSize: 11,
            }}
          />
          {model.peakDay ? (
            <ReferenceLine
              x={model.peakDay}
              stroke="var(--primary)"
              label={{
                value: `peak ${format(model.peakValue)}`,
                position: 'top',
                fill: 'var(--primary)',
                fontSize: 11,
                fontWeight: 600,
              }}
            />
          ) : null}
        </BarChart>
      </ChartContainer>
      <Legend
        items={model.legend.map((item) => ({
          key: item.key,
          label: item.label,
          color: item.color,
          value: format(item.total),
        }))}
      />
    </div>
  )
}
