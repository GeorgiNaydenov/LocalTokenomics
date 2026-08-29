import { useEffect, useId, useRef, useState } from 'react'

export interface Option {
  value: string
  label: string
}

interface MultiSelectProps {
  label: string
  options: Option[]
  selected: string[]
  onChange: (selected: string[]) => void
  emptyLabel?: string
}

/** Hand-built combobox: checkbox list, "all" shortcut, closes on outside click. */
export function MultiSelect({
  label,
  options,
  selected,
  onChange,
  emptyLabel = 'none available',
}: MultiSelectProps) {
  const [open, setOpen] = useState(false)
  const root = useRef<HTMLDivElement>(null)
  const listId = useId()

  useEffect(() => {
    if (!open) return
    const onPointerDown = (event: MouseEvent) => {
      if (root.current && !root.current.contains(event.target as Node)) setOpen(false)
    }
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setOpen(false)
    }
    document.addEventListener('mousedown', onPointerDown)
    document.addEventListener('keydown', onKey)
    return () => {
      document.removeEventListener('mousedown', onPointerDown)
      document.removeEventListener('keydown', onKey)
    }
  }, [open])

  const all = options.length > 0 && selected.length === options.length
  const summary = options.length === 0 ? emptyLabel : all ? `All ${label.toLowerCase()}` : selected.length === 0 ? 'None selected' : selected.length === 1 ? (options.find((option) => option.value === selected[0])?.label ?? '1 selected') : `${selected.length} of ${options.length}`

  const toggle = (value: string) => {
    const next = selected.includes(value)
      ? selected.filter((item) => item !== value)
      : [...selected, value]
    // keep the caller's list in the canonical option order
    onChange(options.filter((option) => next.includes(option.value)).map((option) => option.value))
  }

  return (
    <div ref={root} className="relative">
      <label className="mb-1 block text-[11px] font-medium tracking-wide text-muted uppercase">
        {label}
      </label>
      <button
        type="button"
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-controls={listId}
        disabled={options.length === 0}
        onClick={() => setOpen((value) => !value)}
        className="flex h-[34px] w-full min-w-[150px] items-center justify-between gap-2 rounded-lg border border-border bg-surface px-2.5 text-[13px] text-ink transition-colors hover:bg-surface-2 disabled:opacity-55"
      >
        <span className="truncate">{summary}</span>
        <svg width="10" height="6" viewBox="0 0 10 6" aria-hidden className="shrink-0">
          <path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>
      {open ? (
        <div
          id={listId}
          role="listbox"
          aria-multiselectable
          className="thin-scroll absolute z-30 mt-1 max-h-72 w-max min-w-full overflow-y-auto rounded-lg border border-border bg-popover p-1 shadow-lg"
        >
          <button
            type="button"
            onClick={() => onChange(all ? [] : options.map((option) => option.value))}
            className="mb-1 w-full rounded-md px-2 py-1.5 text-left text-[12px] text-accent hover:bg-track"
          >
            {all ? 'Clear all' : 'Select all'}
          </button>
          {options.map((option) => {
            const checked = selected.includes(option.value)
            return (
              <button
                key={option.value}
                type="button"
                role="option"
                aria-selected={checked}
                onClick={() => toggle(option.value)}
                className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-[13px] text-ink hover:bg-track"
              >
                <span
                  className={`flex h-[15px] w-[15px] shrink-0 items-center justify-center rounded-[4px] border ${
                    checked ? 'border-accent bg-accent' : 'border-border-strong'
                  }`}
                >
                  {checked ? (
                    <svg width="9" height="7" viewBox="0 0 9 7" aria-hidden>
                      <path d="M1 3.6L3.3 6 8 1" fill="none" stroke="white" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  ) : null}
                </span>
                <span className="whitespace-nowrap">{option.label}</span>
              </button>
            )
          })}
        </div>
      ) : null}
    </div>
  )
}
