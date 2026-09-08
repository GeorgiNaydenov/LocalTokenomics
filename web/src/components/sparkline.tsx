import { HoverFrame } from '@/components/chart-hover'
import { cn } from '@/design-system/cn'

function geometry(values: number[], width: number, height: number) {
  const max = Math.max(...values, 1)
  const step = values.length > 1 ? width / (values.length - 1) : width
  const points = values.map(
    (value, index) =>
      `${(index * step).toFixed(1)},${(height - 1.5 - (value / max) * (height - 4)).toFixed(1)}`,
  )
  return { line: points.join(' '), area: `M0,${height} L${points.join(' L')} L${width},${height} Z` }
}

function Chart({
  values,
  width,
  height,
  color,
  fill,
  stretch,
  label,
  hovered,
}: {
  values: number[]
  width: number
  height: number
  color: string
  fill: boolean
  stretch: boolean
  label?: string
  hovered: number | null
}) {
  const { line, area } = geometry(values, width, height)
  const max = Math.max(...values, 1)

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      width={stretch ? '100%' : width}
      height={height}
      preserveAspectRatio={stretch ? 'none' : undefined}
      role={label ? 'img' : 'presentation'}
      aria-label={label}
      className={cn('block shrink-0 overflow-visible')}
    >
      {fill ? <path d={area} fill={color} opacity={0.16} /> : null}
      <polyline
        points={line}
        fill="none"
        stroke={color}
        strokeWidth={1.4}
        vectorEffect="non-scaling-stroke"
      />
      {hovered !== null && values[hovered] !== undefined ? (
        <>
          <line
            x1={(hovered * (values.length > 1 ? width / (values.length - 1) : width)).toFixed(1)}
            x2={(hovered * (values.length > 1 ? width / (values.length - 1) : width)).toFixed(1)}
            y1={0}
            y2={height}
            stroke="var(--muted-foreground)"
            strokeWidth={1}
            strokeOpacity={0.5}
            vectorEffect="non-scaling-stroke"
          />
          <circle
            cx={(hovered * (values.length > 1 ? width / (values.length - 1) : width)).toFixed(1)}
            cy={(height - 1.5 - (values[hovered] / max) * (height - 4)).toFixed(1)}
            r={2.4}
            fill={color}
            stroke="var(--card)"
            strokeWidth={1}
            vectorEffect="non-scaling-stroke"
          />
        </>
      ) : null}
    </svg>
  )
}

export function Sparkline({
  values,
  width = 120,
  height = 26,
  color = 'var(--muted-foreground)',
  fill = false,
  stretch = false,
  label,
  labels,
  format,
  seriesLabel = 'Value',
  className,
}: {
  values: number[]
  width?: number
  height?: number
  color?: string
  fill?: boolean
  stretch?: boolean
  label?: string
  labels?: string[]
  format?: (value: number) => string
  seriesLabel?: string
  className?: string
}) {
  if (values.length === 0) return null

  const chart = (hovered: number | null) => (
    <Chart
      values={values}
      width={width}
      height={height}
      color={color}
      fill={fill}
      stretch={stretch}
      label={labels && format ? undefined : label}
      hovered={hovered}
    />
  )

  if (!labels || !format) return <div className={className}>{chart(null)}</div>

  return (
    <HoverFrame
      count={values.length}
      label={label ?? seriesLabel}
      positionAt={(index) => (values.length > 1 ? index / (values.length - 1) : 0.5)}
      describe={(index) => ({
        title: labels[index] ?? '',
        entries: [{ label: seriesLabel, value: format(values[index]), color }],
      })}
      className={className}
    >
      {chart}
    </HoverFrame>
  )
}
