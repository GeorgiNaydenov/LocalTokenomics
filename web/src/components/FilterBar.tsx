import type { Meta, ReportQuery } from '../api'
import { shiftDays } from '../format'
import { Button, Switch } from './Controls'
import { MultiSelect } from './MultiSelect'

interface FilterBarProps {
  meta: Meta | null
  query: ReportQuery
  onChange: (next: ReportQuery) => void
  onReset: () => void
  dirty: boolean
  modelLabel: (model: string) => string
}

export function FilterBar({
  meta,
  query,
  onChange,
  onReset,
  dirty,
  modelLabel,
}: FilterBarProps) {
  const first = meta?.first_day ?? null
  const last = meta?.last_day ?? null

  const preset = (days: number | null) => {
    if (!first || !last) return
    const since = days === null ? first : maxDay(first, shiftDays(last, -(days - 1)))
    onChange({ ...query, since, until: last })
  }

  const activePreset = (days: number | null): boolean => {
    if (!first || !last) return false
    if (query.until !== last) return false
    if (days === null) return query.since === first
    return query.since === maxDay(first, shiftDays(last, -(days - 1)))
  }

  return (
    <div className="rounded-xl border border-border bg-surface p-4 shadow-[var(--shadow-card)]">
      <div className="flex flex-wrap items-end gap-x-4 gap-y-3">
        <div>
          <label className="mb-1 block text-[11px] font-medium tracking-wide text-muted uppercase">
            From
          </label>
          <input
            type="date"
            value={query.since ?? ''}
            min={first ?? undefined}
            max={query.until ?? last ?? undefined}
            onChange={(event) => onChange({ ...query, since: event.target.value || first })}
            className="tnum h-[34px] rounded-lg border border-border bg-surface px-2.5 text-[13px] text-ink"
          />
        </div>
        <div>
          <label className="mb-1 block text-[11px] font-medium tracking-wide text-muted uppercase">
            To
          </label>
          <input
            type="date"
            value={query.until ?? ''}
            min={query.since ?? first ?? undefined}
            max={last ?? undefined}
            onChange={(event) => onChange({ ...query, until: event.target.value || last })}
            className="tnum h-[34px] rounded-lg border border-border bg-surface px-2.5 text-[13px] text-ink"
          />
        </div>

        <div className="flex h-[34px] items-center gap-1 self-end rounded-lg border border-border bg-track p-0.5">
          {(
            [
              { label: 'Last 7', days: 7 },
              { label: 'Last 30', days: 30 },
              { label: 'All', days: null },
            ] as const
          ).map((item) => (
            <button
              key={item.label}
              type="button"
              aria-pressed={activePreset(item.days)}
              onClick={() => preset(item.days)}
              className={`rounded-[6px] px-2.5 py-1 text-[12.5px] font-medium transition-colors ${
                activePreset(item.days)
                  ? 'bg-raised text-ink shadow-[var(--shadow-card)]'
                  : 'text-muted hover:text-ink'
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>

        <div aria-hidden className="hidden h-8 w-px self-end bg-border xl:block" />

        <MultiSelect
          label="Clients"
          options={(meta?.clients ?? []).map((client) => ({ value: client.id, label: client.label }))}
          selected={query.clients}
          onChange={(clients) => onChange({ ...query, clients })}
        />
        <MultiSelect
          label="Providers"
          options={(meta?.providers ?? []).map((provider) => ({ value: provider, label: provider }))}
          selected={query.providers}
          onChange={(providers) => onChange({ ...query, providers })}
        />
        <MultiSelect
          label="Models"
          options={(meta?.models ?? []).map((model) => ({ value: model, label: modelLabel(model) }))}
          selected={query.models}
          onChange={(models) => onChange({ ...query, models })}
        />
        <MultiSelect
          label="Projects"
          options={(meta?.projects ?? []).map((project) => ({ value: project, label: project }))}
          selected={query.projects}
          onChange={(projects) => onChange({ ...query, projects })}
          emptyLabel="no projects"
        />

        <div className="ml-auto flex items-center gap-3 self-end pb-1">
          <Switch
            checked={query.includeSidechains}
            onChange={(includeSidechains) => onChange({ ...query, includeSidechains })}
            title="Subagent (sidechain) requests are billed too — turn this off to see only main-thread usage."
          >
            Include subagent requests
          </Switch>
          {dirty ? (
            <Button onClick={onReset} className="self-end">
              Reset
            </Button>
          ) : null}
        </div>
      </div>
    </div>
  )
}

function maxDay(a: string, b: string): string {
  return a > b ? a : b
}
