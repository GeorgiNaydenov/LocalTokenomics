import type { ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  className?: string
  padded?: boolean
}

/** The single surface used everywhere: hairline ring, soft radius, no drama. */
export function Card({ children, className = '', padded = true }: CardProps) {
  return (
    <section
      className={`rounded-xl border border-border bg-surface shadow-[var(--shadow-card)] ${
        padded ? 'p-5' : ''
      } ${className}`}
    >
      {children}
    </section>
  )
}

interface CardHeaderProps {
  title: string
  hint?: ReactNode
  actions?: ReactNode
  className?: string
}

export function CardHeader({ title, hint, actions, className = '' }: CardHeaderProps) {
  return (
    <header className={`mb-4 flex flex-wrap items-start justify-between gap-3 ${className}`}>
      <div className="min-w-0">
        <h2 className="text-[13px] font-semibold tracking-wide text-ink uppercase">{title}</h2>
        {hint ? <p className="mt-1 text-[12.5px] leading-snug text-ink-2">{hint}</p> : null}
      </div>
      {actions ? <div className="flex shrink-0 items-center gap-2">{actions}</div> : null}
    </header>
  )
}
