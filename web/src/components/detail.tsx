import type { ReactNode } from 'react'

import { cn } from '@/design-system/cn'
import { StatLabel } from '@/components/stat'

export function Section({
  title,
  action,
  children,
  className,
}: {
  title: string
  action?: ReactNode
  children: ReactNode
  className?: string
}) {
  return (
    <section className={cn('space-y-2.5', className)}>
      <div className="flex items-baseline justify-between gap-3">
        <StatLabel>{title}</StatLabel>
        {action}
      </div>
      {children}
    </section>
  )
}

export function MetaGrid({
  items,
  className,
}: {
  items: { label: string; value: ReactNode }[]
  className?: string
}) {
  return (
    <dl
      className={cn(
        'grid grid-cols-2 gap-x-4 gap-y-3 rounded-md border bg-muted/40 p-3',
        className,
      )}
    >
      {items.map((item) => (
        <div key={item.label} className="min-w-0 space-y-0.5">
          <dt className="text-[10px] uppercase tracking-[0.08em] text-muted-foreground">
            {item.label}
          </dt>
          <dd className="tabular text-xs font-medium break-words">{item.value}</dd>
        </div>
      ))}
    </dl>
  )
}

export function CodeBlock({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <pre
      className={cn(
        'scroll-thin overflow-x-auto rounded-md border bg-muted/50 px-3 py-2.5 text-[11px] leading-relaxed break-words whitespace-pre-wrap',
        className,
      )}
    >
      <code>{children}</code>
    </pre>
  )
}

export function PathList({ paths, className }: { paths: string[]; className?: string }) {
  return (
    <ul className={cn('space-y-1.5', className)}>
      {paths.map((path) => (
        <li
          key={path}
          className="tabular rounded-md border bg-muted/40 px-2.5 py-2 text-[11px] break-all text-muted-foreground"
        >
          {path}
        </li>
      ))}
    </ul>
  )
}
