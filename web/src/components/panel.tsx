import * as React from 'react'

import { cn } from '@/design-system/cn'

export function Panel({ className, ...props }: React.ComponentProps<'section'>) {
  return (
    <section
      data-slot="panel"
      className={cn('rounded-md border bg-card text-card-foreground', className)}
      {...props}
    />
  )
}

export function PanelHeader({
  eyebrow,
  title,
  hint,
  actions,
  className,
}: {
  eyebrow?: React.ReactNode
  title: React.ReactNode
  hint?: React.ReactNode
  actions?: React.ReactNode
  className?: string
}) {
  return (
    <header
      className={cn(
        'flex flex-wrap items-start justify-between gap-3 border-b px-card py-4',
        className,
      )}
    >
      <div className="min-w-0 space-y-1">
        {eyebrow ? (
          <p className="text-[11px] font-medium uppercase tracking-[0.08em] text-primary">
            {eyebrow}
          </p>
        ) : null}
        <h2 className="text-[0.9375rem] font-semibold leading-none tracking-[-0.01em]">
          {title}
        </h2>
        {hint ? (
          <p className="max-w-prose text-xs leading-relaxed text-muted-foreground">{hint}</p>
        ) : null}
      </div>
      {actions ? (
        <div className="flex min-w-0 flex-wrap items-center justify-end gap-2">{actions}</div>
      ) : null}
    </header>
  )
}

export function PanelBody({ className, ...props }: React.ComponentProps<'div'>) {
  return <div className={cn('p-card', className)} {...props} />
}

export function PanelNote({ className, ...props }: React.ComponentProps<'p'>) {
  return (
    <p
      className={cn(
        'border-t px-card py-3 text-xs leading-relaxed text-muted-foreground',
        className,
      )}
      {...props}
    />
  )
}
