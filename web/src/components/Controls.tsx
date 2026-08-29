import type { ButtonHTMLAttributes, ReactNode } from 'react'

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'solid' | 'ghost'
}

export function Button({ variant = 'ghost', className = '', ...rest }: ButtonProps) {
  const base =
    'inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-[13px] font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-55'
  const skin =
    variant === 'solid'
      ? 'bg-accent text-white hover:opacity-90'
      : 'border border-border bg-surface text-ink-2 hover:bg-surface-2 hover:text-ink'
  return <button type="button" className={`${base} ${skin} ${className}`} {...rest} />
}

interface SegmentedProps<T extends string> {
  value: T
  options: { value: T; label: string }[]
  onChange: (value: T) => void
  label?: string
}

export function Segmented<T extends string>({
  value,
  options,
  onChange,
  label,
}: SegmentedProps<T>) {
  return (
    <div className="flex items-center gap-2">
      {label ? <span className="text-[12px] text-muted">{label}</span> : null}
      <div
        role="group"
        aria-label={label}
        className="inline-flex rounded-lg border border-border bg-track p-0.5"
      >
        {options.map((option) => {
          const active = option.value === value
          return (
            <button
              key={option.value}
              type="button"
              aria-pressed={active}
              onClick={() => onChange(option.value)}
              className={`rounded-[6px] px-2.5 py-1 text-[12.5px] font-medium transition-colors ${
                active
                  ? 'bg-raised text-ink shadow-[var(--shadow-card)]'
                  : 'text-muted hover:text-ink'
              }`}
            >
              {option.label}
            </button>
          )
        })}
      </div>
    </div>
  )
}

interface SwitchProps {
  checked: boolean
  onChange: (checked: boolean) => void
  children: ReactNode
  title?: string
}

export function Switch({ checked, onChange, children, title }: SwitchProps) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      title={title}
      onClick={() => onChange(!checked)}
      className="inline-flex items-center gap-2 rounded-lg px-1 py-1 text-[13px] text-ink-2 hover:text-ink"
    >
      <span
        className={`relative h-[18px] w-[32px] shrink-0 rounded-full transition-colors ${
          checked ? 'bg-accent' : 'bg-surface-3'
        }`}
      >
        <span
          className={`absolute top-[2px] h-[14px] w-[14px] rounded-full bg-white transition-all ${
            checked ? 'left-[16px]' : 'left-[2px]'
          }`}
        />
      </span>
      <span>{children}</span>
    </button>
  )
}

/** A colour key that never asks the reader to match hues from memory. */
export function Swatch({ color }: { color: string }) {
  return (
    <span
      aria-hidden
      className="inline-block h-2.5 w-2.5 shrink-0 rounded-[3px]"
      style={{ background: color }}
    />
  )
}
