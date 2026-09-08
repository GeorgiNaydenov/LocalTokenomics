import { useId } from 'react'
import type { CostState, FacetGroup as FacetKey, Meta, OutcomeLabel, Query, Report } from './api'
import { RECENCY_DAYS, isRecent, shiftDays } from './format'
import { ChipRow, DateRange, FacetGroup, SearchField } from '@/components/filters'
import { seriesColor } from '@/components/series'
import { StatLabel } from '@/components/stat'
import { DisclosurePanel } from '@/components/states'
import { COST_STATE_META, OUTCOME_META } from '@/components/status'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Separator } from '@/components/ui/separator'
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle } from '@/components/ui/sheet'
import { Switch } from '@/components/ui/switch'
import { cn } from '@/design-system/cn'

interface RailProps {
  meta: Meta | null
  report: Report | null
  query: Query
  onChange: (patch: Partial<Query>) => void
  onToggleFacet: (group: FacetKey, value: string) => void
  onReset: () => void
  today: string
}

interface FilterRailProps extends RailProps {
  open: boolean
  onClose: () => void
  docked: boolean
}

interface FacetOption<V extends string = string> {
  value: V
  label: string
  color?: string
}

interface FacetEntry {
  value: string
  label: string
  color?: string
  count: number
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

function splitByRecency<E extends { value: string }>(
  entries: E[],
  lastSeen: Record<string, string> | undefined,
  today: string,
): { recent: E[]; stale: E[] } {
  const recent: E[] = []
  const stale: E[] = []
  for (const entry of entries) {
    if (isRecent(lastSeen?.[entry.value], today)) recent.push(entry)
    else stale.push(entry)
  }
  return { recent, stale }
}

const RECENT_CLIENTS = 3

/**
 * Ranks by last_seen instead of a fixed day cutoff. A tool used every few weeks, like an
 * agent you reach for occasionally, should not fall out of view just for missing a fixed
 * window by a day; it only drops off once enough other clients have been more recent.
 */
function topByRecency<E extends { value: string }>(
  entries: E[],
  lastSeen: Record<string, string> | undefined,
  count: number,
): { recent: E[]; stale: E[] } {
  const ranked = [...entries].sort((a, b) => {
    const bSeen = lastSeen?.[b.value] ?? ''
    const aSeen = lastSeen?.[a.value] ?? ''
    return bSeen.localeCompare(aSeen)
  })
  return { recent: ranked.slice(0, count), stale: ranked.slice(count) }
}

function toFacetOption(entry: FacetEntry) {
  return {
    value: entry.value,
    label: entry.label,
    color: entry.color,
    count: entry.count || undefined,
  }
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

function SavedViewChips({
  views,
  query,
  onApply,
}: {
  views: SavedView[]
  query: Query
  onApply: (patch: Partial<Query>) => void
}) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {views.map((view) => {
        const on = matchesPatch(query, view.patch)
        return (
          <button
            key={view.id}
            type="button"
            aria-pressed={on}
            onClick={() => onApply(view.patch)}
            className={cn(
              'rounded-full border px-2.5 py-1 text-xs transition-colors',
              on
                ? 'border-transparent bg-primary-subtle font-medium text-primary'
                : 'text-muted-foreground hover:bg-accent hover:text-foreground',
            )}
          >
            {view.label}
          </button>
        )
      })}
    </div>
  )
}

function SwitchRow({
  label,
  checked,
  onToggle,
}: {
  label: string
  checked: boolean
  onToggle: (next: boolean) => void
}) {
  const id = useId()
  return (
    <div className="flex items-center gap-2.5 rounded-md border bg-card p-2.5">
      <Switch id={id} checked={checked} onCheckedChange={onToggle} />
      <Label htmlFor={id} className="font-normal">
        {label}
      </Label>
    </div>
  )
}

function RailContent({ meta, report, query, onChange, onToggleFacet, onReset, today }: RailProps) {
  const stateOptions: FacetOption<CostState>[] = STATE_VALUES.map((value) => ({
    value,
    label: COST_STATE_META[value].label,
    color: COST_STATE_META[value].color,
  }))
  const stateEntries = buildFacetEntries(stateOptions, report?.facets.states, query.states)

  const outcomeOptions: FacetOption<OutcomeLabel>[] = OUTCOME_VALUES.map((value) => ({
    value,
    label: OUTCOME_META[value].label,
    color: OUTCOME_META[value].color,
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
    color: seriesColor(i),
  }))
  const clientEntries = buildFacetEntries(clientOptions, report?.facets.clients, query.clients)
  const clientSplit = topByRecency(clientEntries, meta?.client_last_seen, RECENT_CLIENTS)

  const modelLabels = new Map((report?.by_model ?? []).map((bucket) => [bucket.key, bucket.label]))
  const modelOptions: FacetOption[] = (meta?.models ?? []).map((model) => ({
    value: model,
    label: modelLabels.get(model) ?? model,
  }))
  const modelEntries = buildFacetEntries(modelOptions, report?.facets.models, query.models)
  const modelSplit = splitByRecency(modelEntries, meta?.model_last_seen, today)

  const projectOptions: FacetOption[] = (meta?.projects ?? []).map((project) => ({
    value: project,
    label: project,
  }))
  const projectEntries = buildFacetEntries(projectOptions, report?.facets.projects, query.projects)
  const projectSplit = splitByRecency(projectEntries, meta?.project_last_seen, today)

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
  const activePreset = RANGE_PRESETS.find(
    (preset) => query.until === today && query.since === presetSince(preset, today, meta),
  )

  return (
    <div className="flex flex-col gap-6">
      <SearchField
        value={query.search}
        onChange={(search) => onChange({ search })}
        placeholder="Search sessions, models, repos"
      />

      <div className="space-y-2">
        <StatLabel>Saved views</StatLabel>
        <SavedViewChips views={views} query={query} onApply={onChange} />
      </div>

      <div className="space-y-2">
        <StatLabel>Range</StatLabel>
        <ChipRow
          options={RANGE_PRESETS.map((preset) => ({ value: preset.label, label: preset.label }))}
          active={activePreset?.label ?? null}
          onSelect={(label) => {
            const preset = RANGE_PRESETS.find((entry) => entry.label === label)
            if (!preset) return
            onChange({ since: presetSince(preset, today, meta), until: today })
          }}
        />
        <DateRange
          since={query.since}
          until={query.until}
          min={meta?.first_day ?? undefined}
          max={meta?.last_day ?? undefined}
          onChange={(patch) => {
            if (patch.since !== undefined) onChange({ since: patch.since || (meta?.first_day ?? null) })
            if (patch.until !== undefined) onChange({ until: patch.until || today })
          }}
        />
      </div>

      <Separator />

      <FacetGroup
        title="Cost state"
        options={stateEntries.map(toFacetOption)}
        selected={query.states}
        onToggle={(value) => onToggleFacet('states', value)}
      />

      <div className="space-y-2">
        <FacetGroup
          title="Outcome"
          options={outcomeEntries.map(toFacetOption)}
          selected={query.outcomes}
          onToggle={(value) => toggleOutcome(value as OutcomeLabel)}
        />
        <p className="text-[11px] leading-relaxed text-muted-foreground">
          Ratings are read at scan time. A session you just rated moves into its bucket after the next rescan.
        </p>
      </div>

      <div className="space-y-2">
        <FacetGroup
          title={`Clients (${clientSplit.recent.length} shown)`}
          options={clientSplit.recent.map(toFacetOption)}
          selected={query.clients}
          onToggle={(value) => onToggleFacet('clients', value)}
        />
        <p className="text-[11px] leading-relaxed text-muted-foreground">
          Only sources found on this machine are listed.
        </p>
        {clientSplit.stale.length > 0 && (
          <DisclosurePanel
            title={`${clientSplit.stale.length} less recently used clients`}
            summary={`Showing your ${RECENT_CLIENTS} most recently active clients by default. Kept out of view, still selectable.`}
          >
            <FacetGroup
              title="All"
              options={clientSplit.stale.map(toFacetOption)}
              selected={query.clients}
              onToggle={(value) => onToggleFacet('clients', value)}
            />
          </DisclosurePanel>
        )}
      </div>

      <div className="space-y-2">
        <div className="scroll-thin max-h-52 overflow-y-auto">
          <FacetGroup
            title="Models"
            options={modelSplit.recent.map(toFacetOption)}
            selected={query.models}
            onToggle={(value) => onToggleFacet('models', value)}
          />
        </div>
        {modelSplit.stale.length > 0 && (
          <DisclosurePanel
            title={`${modelSplit.stale.length} models not used in ${RECENCY_DAYS} days`}
            summary="Kept out of the default view, still selectable."
          >
            <div className="scroll-thin max-h-52 overflow-y-auto">
              <FacetGroup
                title="All"
                options={modelSplit.stale.map(toFacetOption)}
                selected={query.models}
                onToggle={(value) => onToggleFacet('models', value)}
              />
            </div>
          </DisclosurePanel>
        )}
      </div>

      <div className="space-y-2">
        <div className="scroll-thin max-h-52 overflow-y-auto">
          <FacetGroup
            title="Projects"
            options={projectSplit.recent.map(toFacetOption)}
            selected={query.projects}
            onToggle={(value) => onToggleFacet('projects', value)}
          />
        </div>
        {projectSplit.stale.length > 0 && (
          <DisclosurePanel
            title={`${projectSplit.stale.length} projects not used in ${RECENCY_DAYS} days`}
            summary="Kept out of the default view, still selectable."
          >
            <div className="scroll-thin max-h-52 overflow-y-auto">
              <FacetGroup
                title="All"
                options={projectSplit.stale.map(toFacetOption)}
                selected={query.projects}
                onToggle={(value) => onToggleFacet('projects', value)}
              />
            </div>
          </DisclosurePanel>
        )}
      </div>

      <div className="space-y-2">
        <SwitchRow
          label="Include subagent requests"
          checked={query.includeSidechains}
          onToggle={(next) => onChange({ includeSidechains: next })}
        />
        <SwitchRow
          label="Traced only"
          checked={query.traced === true}
          onToggle={(next) => onChange({ traced: next ? true : null })}
        />
        <SwitchRow
          label="Errors only"
          checked={query.hasErrors === true}
          onToggle={(next) => onChange({ hasErrors: next ? true : null })}
        />
      </div>

      {dirty && (
        <Button variant="outline" size="sm" onClick={onReset} className="w-full">
          Clear all filters
        </Button>
      )}

      {undetected.length > 0 && (
        <DisclosurePanel
          title={`${undetected.length} sources not detected here`}
          summary="Not installed here, so they are kept out of every filter and total. Point one at a log path to bring it in."
        >
          <div className="space-y-2">
            {undetected.map((source) => (
              <div key={source.id} className="space-y-1 rounded-md border p-2.5">
                <div className="text-xs text-muted-foreground">{source.label}</div>
                <div className="tabular text-[10px] break-all text-muted-foreground">{source.path}</div>
                <div className="tabular text-[10px] break-all text-muted-foreground">{source.root_hint}</div>
              </div>
            ))}
          </div>
        </DisclosurePanel>
      )}
    </div>
  )
}

export default function FilterRail({ open, onClose, docked, ...rail }: FilterRailProps) {
  return (
    <>
      <aside
        className={cn(
          'scroll-thin sticky top-[52px] max-h-[calc(100vh-52px)] hidden w-[266px] shrink-0 overflow-y-auto border-r bg-muted/40 p-4',
          docked && 'lg:block',
        )}
      >
        <RailContent {...rail} />
      </aside>

      <Sheet
        open={open}
        onOpenChange={(next) => {
          if (!next) onClose()
        }}
      >
        <SheetContent side="left" className="w-[300px] gap-0 p-0">
          <SheetHeader className="border-b">
            <SheetTitle className="text-sm">Filters</SheetTitle>
            <SheetDescription className="text-[11px]">
              Narrow the slice by date, cost state, outcome, client, model and project.
            </SheetDescription>
          </SheetHeader>
          <div className="scroll-thin min-h-0 flex-1 overflow-y-auto p-4">
            <RailContent {...rail} />
          </div>
        </SheetContent>
      </Sheet>
    </>
  )
}
