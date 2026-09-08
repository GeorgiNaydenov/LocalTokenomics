import type { ContextSnapshot } from './api'
import {
  formatClock,
  formatDayShort,
  formatMoney,
  formatMoneyShort,
  formatPercent,
  formatTokens,
} from './format'
import { SERIES } from './theme'

export interface ChartBar {
  x: number
  y: number
  w: number
  h: number
  fill: string
  title: string
}

export interface ChartTick {
  y: number
  top: number
  label: string
}

export interface ChartXTick {
  left: number
  label: string
}

export interface ChartLegendItem {
  label: string
  color: string
  value: string
  key: string
}

export interface TimeChart {
  bars: ChartBar[]
  grid: ChartTick[]
  w: number
  h: number
  right: number
  xLabelTop: number
  meanY: number
  meanLabel: string
  peakX: number
  peakY: number
  peakLineY: number
  peakLabelTop: number
  peakLabelLeft: number
  peakLabelTransform: string
  peakLabel: string
  xTicks: ChartXTick[]
  legend: ChartLegendItem[]
  title: string
  note: string
}

export interface TimeChartRow {
  day: string
  key: string
  label: string
  value: number
}

export interface TimeChartParams {
  days: string[]
  rows: TimeChartRow[]
  chartWidth: number
  isCost: boolean
  stackByLabel: string
}

const PAD_L = 52
const PAD_R = 14
const TOP = 30
const BOTTOM = 208
const HEIGHT = 240
const X_LABEL_TOP = 216

function round1(value: number): number {
  return Math.round(value * 10) / 10
}

export function timeChart(params: TimeChartParams): TimeChart {
  const { days, rows, chartWidth, isCost, stackByLabel } = params
  const fmtFull = isCost ? formatMoney : formatTokens
  const fmtShort = isCost ? formatMoneyShort : formatTokens

  const totalsByKey = new Map<string, number>()
  const labels = new Map<string, string>()
  for (const row of rows) {
    totalsByKey.set(row.key, (totalsByKey.get(row.key) ?? 0) + row.value)
    labels.set(row.key, row.label)
  }
  const keys = [...totalsByKey.entries()].sort((a, b) => b[1] - a[1]).map(([key]) => key)

  const grid = new Map<string, Map<string, number>>(days.map((day) => [day, new Map()]))
  for (const row of rows) {
    const dayMap = grid.get(row.day)
    if (!dayMap) continue
    dayMap.set(row.key, (dayMap.get(row.key) ?? 0) + row.value)
  }
  const dayTotals = days.map((day) =>
    [...(grid.get(day)?.values() ?? [])].reduce((a, b) => a + b, 0),
  )
  const max = Math.max(...dayTotals, 1)

  const w = Math.max(280, chartWidth)
  const step = (w - PAD_L - PAD_R) / Math.max(days.length, 1)
  const barW = step > 6 ? step - 3 : Math.max(1, step * 0.85)
  const y = (value: number) => BOTTOM - (value / max) * (BOTTOM - TOP)

  const bars: ChartBar[] = []
  days.forEach((day, i) => {
    let acc = 0
    const dayMap = grid.get(day)
    keys.forEach((key) => {
      const value = dayMap?.get(key) ?? 0
      if (value <= 0) return
      const y0 = y(acc + value)
      const y1 = y(acc)
      bars.push({
        x: round1(PAD_L + i * step + (step - barW) / 2),
        y: round1(y0),
        w: round1(barW),
        h: round1(Math.max(0.8, y1 - y0)),
        fill: SERIES[keys.indexOf(key) % SERIES.length],
        title: `${formatDayShort(day)} · ${labels.get(key) ?? key} · ${fmtFull(value)}`,
      })
      acc += value
    })
  })

  const mean = dayTotals.reduce((a, b) => a + b, 0) / Math.max(days.length, 1)
  const peakIndex = dayTotals.indexOf(Math.max(...dayTotals))
  const peakX = PAD_L + peakIndex * step + step / 2
  const peakY = y(dayTotals[peakIndex] ?? 0)
  const near = peakX > w - 190

  const gridTicks: ChartTick[] = [0, 0.25, 0.5, 0.75, 1].map((fraction) => ({
    y: round1(y(max * fraction)),
    top: round1(y(max * fraction) - 6),
    label: fmtShort(max * fraction),
  }))

  const stride = Math.max(1, Math.ceil(days.length / 8))
  const xTicks: ChartXTick[] = days
    .filter((_, i) => i % stride === 0 || i === days.length - 1)
    .map((day) => ({
      left: round1(PAD_L + days.indexOf(day) * step + step / 2),
      label: formatDayShort(day),
    }))

  const legend: ChartLegendItem[] = keys.slice(0, 7).map((key, i) => ({
    label: labels.get(key) ?? key,
    color: SERIES[i % SERIES.length],
    value: fmtFull(totalsByKey.get(key) ?? 0),
    key,
  }))

  return {
    bars,
    grid: gridTicks,
    w,
    h: HEIGHT,
    right: w - PAD_R,
    xLabelTop: X_LABEL_TOP,
    meanY: round1(y(mean)),
    meanLabel: `mean ${fmtShort(mean)} per day`,
    peakX: round1(peakX),
    peakY: round1(peakY),
    peakLineY: round1(Math.max(TOP - 16, peakY - 18)),
    peakLabelTop: round1(Math.max(TOP - 30, peakY - 34)),
    peakLabelLeft: round1(near ? peakX - 8 : peakX + 8),
    peakLabelTransform: near ? 'translateX(-100%)' : 'none',
    peakLabel: `peak ${formatDayShort(days[peakIndex] ?? '')} ${fmtFull(dayTotals[peakIndex] ?? 0)}`,
    xTicks,
    legend,
    title: `Daily totals stacked by ${stackByLabel}, ${days.length} days`,
    note: 'Bars are one day. The dashed line is the slice mean. Gaps are days with no logged requests.',
  }
}

export interface ContextBar {
  spanId: string
  x: number
  y: number
  w: number
  h: number
  fill: string
  unknown: boolean
  compactedBefore: boolean
  title: string
}

export interface ContextBars {
  bars: ContextBar[]
  w: number
  h: number
  maxY: number | null
  maxLabel: string
  meanY: number | null
  meanLabel: string
  known: number
  unknown: number
}

const HIGH_OCCUPANCY = 0.85

export function contextBars(snapshots: ContextSnapshot[], w: number, h: number): ContextBars {
  const step = w / Math.max(snapshots.length, 1)
  const barW = step > 6 ? step - 2 : Math.max(1, step * 0.85)
  const y = (fraction: number) => h - Math.min(fraction, 1) * h

  const bars: ContextBar[] = snapshots.map((snapshot, i) => {
    const x = round1(i * step + (step - barW) / 2)
    const scale =
      snapshot.input_total === null || snapshot.capacity === null
        ? ''
        : ` · ${formatTokens(snapshot.input_total)} of ${formatTokens(snapshot.capacity)}`
    const when = formatClock(snapshot.started_at)
    if (snapshot.occupancy === null) {
      return {
        spanId: snapshot.span_id,
        x,
        y: 0,
        w: round1(barW),
        h: round1(h),
        fill: 'var(--border-strong)',
        unknown: true,
        compactedBefore: snapshot.compacted_before,
        title: `${when} · occupancy unavailable${scale}`,
      }
    }
    const top = y(snapshot.occupancy)
    return {
      spanId: snapshot.span_id,
      x,
      y: round1(Math.min(top, h - 0.8)),
      w: round1(barW),
      h: round1(Math.max(0.8, h - top)),
      fill:
        snapshot.occupancy >= HIGH_OCCUPANCY ? 'var(--bubble-c-3)' : 'var(--accent)',
      unknown: false,
      compactedBefore: snapshot.compacted_before,
      title: `${when} · ${formatPercent(snapshot.occupancy)} of context${scale}`,
    }
  })

  const known = snapshots
    .map((snapshot) => snapshot.occupancy)
    .filter((value): value is number => value !== null)
  if (known.length === 0) {
    return {
      bars,
      w,
      h,
      maxY: null,
      maxLabel: 'occupancy unavailable',
      meanY: null,
      meanLabel: 'occupancy unavailable',
      known: 0,
      unknown: snapshots.length,
    }
  }
  const max = Math.max(...known)
  const mean = known.reduce((a, b) => a + b, 0) / known.length
  return {
    bars,
    w,
    h,
    maxY: round1(y(max)),
    maxLabel: `peak ${formatPercent(max)}`,
    meanY: round1(y(mean)),
    meanLabel: `mean ${formatPercent(mean)}`,
    known: known.length,
    unknown: snapshots.length - known.length,
  }
}

export function spark(values: number[], w: number, h: number): { line: string; area: string } {
  const max = Math.max(...values, 1)
  const step = values.length > 1 ? w / (values.length - 1) : w
  const pts = values.map(
    (v, i) => `${(i * step).toFixed(1)},${(h - 1.5 - (v / max) * (h - 4)).toFixed(1)}`,
  )
  return { line: pts.join(' '), area: `M0,${h} L${pts.join(' L')} L${w},${h} Z` }
}
