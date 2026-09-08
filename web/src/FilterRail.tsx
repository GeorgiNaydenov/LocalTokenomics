import { useState } from 'react'
import type { CostState, FacetGroup, Meta, OutcomeLabel, Query, Report } from './api'
import { formatCount, shiftDays } from './format'
import { SERIES, STATE_COLOR } from './theme'

interface FilterRailProps {
  meta: Meta | null
  report: Report | null
  query: Query
  onChange: (patch: Partial<Query>) => void
  onToggleFacet: (group: FacetGroup, value: string) => void
  onReset: () => void
  today: string
  open: boolean
  onClose: () => void
}

interface FacetOption<V extends string = string> {
  value: V
  label: string
  color?: string
}

interface SavedView {
  id: string
  label: string
  patch: Partial<Query>
}

interface RangePreset {
  label: string
  days: number | null
}

const RANGE_PRESETS: RangePreset[] = [
  { label: 'Today', days: 1 },
  { label: '14 d', days: 14 },
  { label: '30 d', days: 30 },
  { label: '60 d', days: 60 },
  { label: '90 d', days: 90 },
  { label: '180 d', days: 180 },
  { label: 'All', days: null },
]

const STATE_VALUES: CostState[] = ['priced', 'free', 'unpriced', 'unavailable']

const OUTCOME_VALUES: OutcomeLabel[] = ['successful', 'partial', 'failed', 'abandoned', 'unrated']

const OUTCOME_COLOR: Record<OutcomeLabel, string> = {
  successful: 'var(--success)',
  partial: 'var(--bubble-c-3)',
  failed: 'var(--rose)',
  abandoned: 'var(--bubble-c-4)',
  unrated: 'var(--border-strong)',
}

function buildFacetEntries<V extends string>(
  options: FacetOption<V>[],
  counts: Record<string, number> | undefined,
  selected: readonly V[],
): (FacetOption<V> & { count: number })[] {
  return options
    .map((option) => ({ ...option, count: counts?.[option.value] ?? 0 }))
    .filter((option) => option.count > 0 || selected.includes(option.value))
    .sort((a, b) => b.count - a.count)
}

function arraysMatch(a: readonly string[], b: readonly string[]): boolean {
  if (a.length !== b.length) return false
  const sortedA = [...a].sort()
  const sortedB = [...b].sort()
  return sortedA.every((value, i) => value === sortedB[i])
}

function matchesPatch(query: Query, patch: Partial<Query>): boolean {
  return (Object.keys(patch) as (keyof Query)[]).every((key) => {
    const current = query[key]
    const target = patch[key]
    if (Array.isArray(current) && Array.isArray(target)) return arraysMatch(current, target)
    return current === target
  })
}

function presetSince(preset: RangePreset, today: string, meta: Meta | null): string {
  if (preset.days === null) return meta?.first_day ?? today
  return shiftDays(today, -(preset.days - 1))
}

function buildSavedViews(meta: Meta | null, report: Report | null, today: string): SavedView[] {
  const views: SavedView[] = [
    {
      id: 'all',
      label: 'All usage',
      patch: {
        search: '',
        states: [],
        clients: [],
        models: [],
        projects: [],
        includeSidechains: true,
        outcomes: [],
        traced: null,
        hasErrors: null,
        since: meta?.first_day ?? today,
        until: today,
      },
    },
    { id: 'week', label: 'Last 7 days', patch: { since: shiftDays(today, -6), until: today } },
    { id: 'gaps', label: 'Missing token data', patch: { states: ['unpriced', 'unavailable'], models: [] } },
    { id: 'main', label: 'Main thread only', patch: { includeSidechains: false } },
    { id: 'trouble', label: 'Sessions with errors', patch: { hasErrors: true } },
  ]
  const top = report?.by_model[0]
  if (top) {
    views.push({ id: 'top-model', label: 'Top model', patch: { models: [top.key], states: [] } })
  }
  return views
}

function FacetOptionButton({
  entry,
  active,
  onToggle,
}: {
  entry: { value: string; label: string; color?: string; count: number }
  active: boolean
  onToggle: () => void
}) {
  return (
    <button type="button" className={'filter-option' + (active ? ' is-active' : '')} onClick={onToggle}>
      <span className="filter-option__choice">
        <span className="filter-option__check">
          {active && (
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={3}>
              <path d="M5 13l4 4L19 7" />
            </svg>
          )}
        </span>
        {entry.color && <span style={{ width: 8, height: 8, flex: 'none', background: entry.color }} />}
        <span className="filter-option__label">{entry.label}</span>
      </span>
      {entry.count > 0 && <span className="filter-option__count num">{formatCount(entry.count)}</span>}
    </button>
  )
}

function Toggle({
  checked,
  onToggle,
  label,
}: {
  checked: boolean
  onToggle: (next: boolean) => void
  label: string
}) {
  return (
    <label
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 8,
        marginTop: 4,
        padding: 8,
        border: '1px solid var(--border)',
        background: 'var(--bg-panel)',
        cursor: 'pointer',
      }}
    >
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onToggle(e.target.checked)}
        style={{ accentColor: 'var(--accent)', width: 14, height: 14 }}
      />
      <span style={{ fontSize: 11.5, color: 'var(--fg-strong)' }}>{label}</span>
    </label>
  )
}

export default function FilterRail({
  meta,
  report,
  query,
  onChange,
  onToggleFacet,
  onReset,
  today,
  open,
  onClose,
}: FilterRailProps) {
  const [undetectedOpen, setUndetectedOpen] = useState(false)

  const stateOptions: FacetOption<CostState>[] = STATE_VALUES.map((value) => ({
    value,
    label: value,
    color: STATE_COLOR[value],
  }))
  const stateEntries = buildFacetEntries(stateOptions, report?.facets.states, query.states)

  const outcomeOptions: FacetOption<OutcomeLabel>[] = OUTCOME_VALUES.map((value) => ({
    value,
    label: value,
    color: OUTCOME_COLOR[value],
  }))
  const outcomeEntries = buildFacetEntries(outcomeOptions, report?.facets.outcomes, query.outcomes)
  const toggleOutcome = (value: OutcomeLabel) => {
    const next = query.outcomes.includes(value)
      ? query.outcomes.filter((current) => current !== value)
      : [...query.outcomes, value]
    onChange({ outcomes: next })
  }

  const clientOptions: FacetOption[] = (meta?.clients ?? []).map((client, i) => ({
    value: client.id,
    label: client.label,
    color: SERIES[i % SERIES.length],
  }))
  const clientEntries = buildFacetEntries(clientOptions, report?.facets.clients, query.clients)

  const modelLabels = new Map((report?.by_model ?? []).map((bucket) => [bucket.key, bucket.label]))
  const modelOptions: FacetOption[] = (meta?.models ?? []).map((model) => ({
    value: model,
    label: modelLabels.get(model) ?? model,
  }))
  const modelEntries = buildFacetEntries(modelOptions, report?.facets.models, query.models)

  const projectOptions: FacetOption[] = (meta?.projects ?? []).map((project) => ({
    value: project,
    label: project,
  }))
  const projectEntries = buildFacetEntries(projectOptions, report?.facets.projects, query.projects)

  const undetected = (meta?.sources ?? []).filter((source) => !source.detected)

  const resetPatch: Partial<Query> = {
    search: '',
    states: [],
    clients: [],
    models: [],
    projects: [],
    includeSidechains: true,
    outcomes: [],
    traced: null,
    hasErrors: null,
    since: meta?.first_day ?? today,
    until: today,
  }
  const dirty = !matchesPatch(query, resetPatch)

  const views = buildSavedViews(meta, report, today)

  const content = (
    <>
      <div className="search-field">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
          <circle cx="11" cy="11" r="7" />
          <path d="m20 20-3.5-3.5" />
        </svg>
        <input
          type="search"
          placeholder="Search sessions, models, repos"
          value={query.search}
          onChange={(e) => onChange({ search: e.target.value })}
        />
      </div>

      <div className="filter-group" style={{ marginTop: 16 }}>
        <div className="filter-group__title">Saved views</div>
        <div className="chip-row">
          {views.map((view) => (
            <button
              key={view.id}
              type="button"
              className={'chip' + (matchesPatch(query, view.patch) ? ' is-active' : '')}
              onClick={() => onChange(view.patch)}
            >
              {view.label}
            </button>
          ))}
        </div>
      </div>

      <div className="filter-group">
        <div className="filter-group__title">Range</div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
          {RANGE_PRESETS.map((preset) => {
            const since = presetSince(preset, today, meta)
            const active = query.until === today && query.since === since
            return (
              <button
                key={preset.label}
                type="button"
                className={'chip' + (active ? ' is-active' : '')}
                onClick={() => onChange({ since, until: today })}
              >
                {preset.label}
              </button>
            )
          })}
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6, marginTop: 8 }}>
          <input
            type="date"
            className="date-input"
            value={query.since ?? ''}
            min={meta?.first_day ?? undefined}
            max={query.until ?? meta?.last_day ?? undefined}
            onChange={(e) => onChange({ since: e.target.value || (meta?.first_day ?? null) })}
          />
          <input
            type="date"
            className="date-input"
            value={query.until ?? ''}
            min={query.since ?? meta?.first_day ?? undefined}
            max={meta?.last_day ?? undefined}
            onChange={(e) => onChange({ until: e.target.value || today })}
          />
        </div>
      </div>

      <div className="filter-group">
        <div className="filter-group__title">Cost state</div>
        {stateEntries.map((entry) => (
          <FacetOptionButton
            key={entry.value}
            entry={entry}
            active={query.states.includes(entry.value)}
            onToggle={() => onToggleFacet('states', entry.value)}
          />
        ))}
      </div>

      <div className="filter-group">
        <div className="filter-group__title">Outcome</div>
        {outcomeEntries.map((entry) => (
          <FacetOptionButton
            key={entry.value}
            entry={entry}
            active={query.outcomes.includes(entry.value)}
            onToggle={() => toggleOutcome(entry.value)}
          />
        ))}
        <p style={{ margin: '6px 0 0', fontSize: 10.5, lineHeight: 1.45, color: 'var(--fg-faint)' }}>
          Ratings are read at scan time. A session you just rated moves into its bucket after the next rescan.
        </p>
      </div>

      <div className="filter-group">
        <div className="filter-group__title">
          Clients<span className="filter-group__selected">{clientEntries.length} shown</span>
        </div>
        {clientEntries.map((entry) => (
          <FacetOptionButton
            key={entry.value}
            entry={entry}
            active={query.clients.includes(entry.value)}
            onToggle={() => onToggleFacet('clients', entry.value)}
          />
        ))}
        <p style={{ margin: '6px 0 0', fontSize: 10.5, lineHeight: 1.45, color: 'var(--fg-faint)' }}>
          Only sources found on this machine are listed.
        </p>
      </div>

      <div className="filter-group">
        <div className="filter-group__title">Models</div>
        <div style={{ maxHeight: 190, overflowY: 'auto' }}>
          {modelEntries.map((entry) => (
            <FacetOptionButton
              key={entry.value}
              entry={entry}
              active={query.models.includes(entry.value)}
              onToggle={() => onToggleFacet('models', entry.value)}
            />
          ))}
        </div>
      </div>

      <div className="filter-group">
        <div className="filter-group__title">Projects</div>
        <div style={{ maxHeight: 190, overflowY: 'auto' }}>
          {projectEntries.map((entry) => (
            <FacetOptionButton
              key={entry.value}
              entry={entry}
              active={query.projects.includes(entry.value)}
              onToggle={() => onToggleFacet('projects', entry.value)}
            />
          ))}
        </div>
      </div>

      <Toggle
        checked={query.includeSidechains}
        onToggle={(next) => onChange({ includeSidechains: next })}
        label="Include subagent requests"
      />
      <Toggle
        checked={query.traced === true}
        onToggle={(next) => onChange({ traced: next ? true : null })}
        label="Traced only"
      />
      <Toggle
        checked={query.hasErrors === true}
        onToggle={(next) => onChange({ hasErrors: next ? true : null })}
        label="Errors only"
      />

      {dirty && (
        <button
          type="button"
          className="btn-ghost"
          onClick={onReset}
          style={{ width: '100%', height: 32, minHeight: 32, marginTop: 10, fontSize: 11.5 }}
        >
          Clear all filters
        </button>
      )}

      {undetected.length > 0 && (
        <div style={{ marginTop: 20, paddingTop: 12, borderTop: '1px solid var(--border)' }}>
          <button
            type="button"
            onClick={() => setUndetectedOpen((o) => !o)}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              width: '100%',
              padding: 0,
              border: 0,
              background: 'none',
              cursor: 'pointer',
              color: 'var(--fg-faint)',
              fontFamily: 'var(--font-sans)',
              fontSize: 10.5,
              textAlign: 'left',
            }}
          >
            <span>{undetected.length} sources not detected here</span>
            <span className="num">{undetectedOpen ? '−' : '+'}</span>
          </button>
          {undetectedOpen && (
            <div style={{ marginTop: 8, display: 'flex', flexDirection: 'column', gap: 6 }}>
              {undetected.map((source) => (
                <div key={source.id} style={{ padding: '7px 8px', border: '1px dashed var(--border-strong)' }}>
                  <div style={{ fontSize: 11, color: 'var(--fg-muted)' }}>{source.label}</div>
                  <div className="num" style={{ fontSize: 9.5, color: 'var(--fg-faint)', marginTop: 2, wordBreak: 'break-all' }}>
                    {source.path}
                  </div>
                  <div className="num" style={{ fontSize: 9.5, color: 'var(--fg-faint)', marginTop: 2, wordBreak: 'break-all' }}>
                    {source.root_hint}
                  </div>
                </div>
              ))}
              <p style={{ margin: '2px 0 0', fontSize: 10, lineHeight: 1.5, color: 'var(--fg-faint)' }}>
                Not installed here, so they are kept out of every filter and total. Point one at a log path to bring
                it in.
              </p>
            </div>
          )}
        </div>
      )}
    </>
  )

  return (
    <>
      <aside className="app-rail">{content}</aside>
      {open && (
        <div className="detail-panel-overlay" onClick={onClose}>
          <aside className="detail-panel drawer" onClick={(e) => e.stopPropagation()}>
            <div className="detail-panel__header">
              <p className="lbl" style={{ color: 'var(--accent)' }}>
                Filters
              </p>
              <button type="button" className="icon-button" onClick={onClose} aria-label="Close filters">
                ×
              </button>
            </div>
            <div className="detail-panel__body">{content}</div>
          </aside>
        </div>
      )}
    </>
  )
}
