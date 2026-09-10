import { useState } from 'react'
import type { ReactNode } from 'react'
import { ColumnsIcon } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

export interface Column<T> {
  key: string
  label: string
  align: 'left' | 'right'
  cell: (row: T) => ReactNode
  cellClassName?: string
}

function readHidden(storageKey: string): Set<string> {
  try {
    const raw = localStorage.getItem(storageKey)
    if (!raw) return new Set()
    const parsed: unknown = JSON.parse(raw)
    return Array.isArray(parsed) ? new Set(parsed.filter((key): key is string => typeof key === 'string')) : new Set()
  } catch {
    return new Set()
  }
}

function persistHidden(storageKey: string, hidden: Set<string>) {
  try {
    localStorage.setItem(storageKey, JSON.stringify([...hidden]))
  } catch {
    return
  }
}

export function useHiddenColumns(storageKey: string): [Set<string>, (key: string) => void] {
  const [hidden, setHidden] = useState<Set<string>>(() => readHidden(storageKey))

  const toggle = (key: string) => {
    setHidden((current) => {
      const next = new Set(current)
      if (next.has(key)) next.delete(key)
      else next.add(key)
      persistHidden(storageKey, next)
      return next
    })
  }

  return [hidden, toggle]
}

export function visibleColumns<T>(columns: Column<T>[], hidden: Set<string>): Column<T>[] {
  const shown = columns.filter((column) => !hidden.has(column.key))
  return shown.length > 0 ? shown : columns
}

export function ColumnChooser<T>({
  columns,
  hidden,
  onToggle,
}: {
  columns: Column<T>[]
  hidden: Set<string>
  onToggle: (key: string) => void
}) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="sm">
          <ColumnsIcon />
          Columns
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-48">
        <DropdownMenuLabel>Shown columns</DropdownMenuLabel>
        <DropdownMenuSeparator />
        {columns.map((column) => (
          <DropdownMenuCheckboxItem
            key={column.key}
            checked={!hidden.has(column.key)}
            onCheckedChange={() => onToggle(column.key)}
            onSelect={(event) => event.preventDefault()}
          >
            {column.label}
          </DropdownMenuCheckboxItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
