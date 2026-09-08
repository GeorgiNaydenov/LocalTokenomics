import * as React from 'react'
import { SearchIcon, XIcon } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { StatLabel } from '@/components/stat'
import { cn } from '@/design-system/cn'

export function SearchField({
  value,
  onChange,
  placeholder = 'Search',
  className,
}: {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  className?: string
}) {
  return (
    <div className={cn('relative', className)}>
      <SearchIcon
        aria-hidden
        className="pointer-events-none absolute left-2.5 top-1/2 size-4 -translate-y-1/2 text-muted-foreground"
      />
      <Input
        type="search"
        value={value}
        placeholder={placeholder}
        onChange={(event) => onChange(event.target.value)}
        className="pl-8"
      />
      {value ? (
        <button
          type="button"
          aria-label="Clear search"
          onClick={() => onChange('')}
          className="absolute right-2 top-1/2 grid size-5 -translate-y-1/2 place-items-center rounded-sm text-muted-foreground hover:text-foreground"
        >
          <XIcon className="size-3.5" />
        </button>
      ) : null}
    </div>
  )
}

export interface FacetOption {
  value: string
  label: string
  count?: number
  color?: string
}

export function FacetGroup({
  title,
  options,
  selected,
  onToggle,
  className,
}: {
  title: string
  options: FacetOption[]
  selected: string[]
  onToggle: (value: string) => void
  className?: string
}) {
  const id = React.useId()

  return (
    <fieldset className={cn('space-y-2', className)}>
      <legend className="mb-2">
        <StatLabel>{title}</StatLabel>
      </legend>
      <div className="space-y-0.5">
        {options.map((option) => {
          const optionId = `${id}-${option.value}`
          return (
            <div
              key={option.value}
              className="flex items-center gap-2.5 rounded-sm px-1.5 py-1.5 hover:bg-accent"
            >
              <Checkbox
                id={optionId}
                checked={selected.includes(option.value)}
                onCheckedChange={() => onToggle(option.value)}
              />
              {option.color ? (
                <span
                  aria-hidden
                  className="size-2 shrink-0 rounded-full"
                  style={{ background: option.color }}
                />
              ) : null}
              <Label
                htmlFor={optionId}
                className="min-w-0 flex-1 cursor-pointer truncate font-normal"
              >
                {option.label}
              </Label>
              {option.count !== undefined ? (
                <span className="tabular text-xs text-muted-foreground">{option.count.toLocaleString()}</span>
              ) : null}
            </div>
          )
        })}
      </div>
    </fieldset>
  )
}

export function ChipRow({
  options,
  active,
  onSelect,
  className,
}: {
  options: { value: string; label: string }[]
  active: string | null
  onSelect: (value: string) => void
  className?: string
}) {
  return (
    <div className={cn('flex flex-wrap gap-1.5', className)}>
      {options.map((option) => {
        const on = option.value === active
        return (
          <button
            key={option.value}
            type="button"
            aria-pressed={on}
            onClick={() => onSelect(option.value)}
            className={cn(
              'rounded-full border px-2.5 py-1 text-xs transition-colors',
              on
                ? 'border-transparent bg-primary-subtle font-medium text-primary'
                : 'text-muted-foreground hover:bg-accent hover:text-foreground',
            )}
          >
            {option.label}
          </button>
        )
      })}
    </div>
  )
}

export function DateRange({
  since,
  until,
  min,
  max,
  onChange,
  className,
}: {
  since: string | null
  until: string | null
  min?: string
  max?: string
  onChange: (patch: { since?: string; until?: string }) => void
  className?: string
}) {
  return (
    <div className={cn('flex flex-wrap gap-2', className)}>
      <Input
        type="date"
        aria-label="From"
        value={since ?? ''}
        min={min}
        max={until ?? max}
        onChange={(event) => onChange({ since: event.target.value })}
        className="tabular h-8 min-w-[7.5rem] flex-1 text-xs"
      />
      <Input
        type="date"
        aria-label="To"
        value={until ?? ''}
        min={since ?? min}
        max={max}
        onChange={(event) => onChange({ until: event.target.value })}
        className="tabular h-8 min-w-[7.5rem] flex-1 text-xs"
      />
    </div>
  )
}

export function SortSelect({
  options,
  value,
  onChange,
  className,
}: {
  options: { value: string; label: string }[]
  value: string
  onChange: (value: string) => void
  className?: string
}) {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger size="sm" className={cn('w-56', className)} aria-label="Sort sessions">
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        {options.map((option) => (
          <SelectItem key={option.value} value={option.value}>
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}

export interface ActiveFilter {
  key: string
  group: string
  label: string
  onRemove: () => void
}

export function FilterChips({
  filters,
  onClear,
  className,
}: {
  filters: ActiveFilter[]
  onClear?: () => void
  className?: string
}) {
  if (filters.length === 0) return null

  return (
    <div className={cn('flex flex-wrap items-center gap-1.5', className)}>
      {filters.map((filter) => (
        <Badge key={filter.key} variant="outline" className="gap-1 py-1 pr-1 pl-2">
          <span className="text-muted-foreground">{filter.group}</span>
          <span className="max-w-40 truncate font-medium">{filter.label}</span>
          <button
            type="button"
            aria-label={`Remove ${filter.group} filter ${filter.label}`}
            onClick={filter.onRemove}
            className="grid size-4 place-items-center rounded-full text-muted-foreground hover:bg-muted hover:text-foreground"
          >
            <XIcon className="size-3" />
          </button>
        </Badge>
      ))}
      {onClear ? (
        <button
          type="button"
          onClick={onClear}
          className="ml-1 text-xs text-muted-foreground underline-offset-4 hover:text-foreground hover:underline"
        >
          Clear all
        </button>
      ) : null}
    </div>
  )
}
