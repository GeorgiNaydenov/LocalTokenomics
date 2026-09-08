import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Separator } from '@/components/ui/separator'
import { Sheet, SheetContent, SheetHeader, SheetTitle } from '@/components/ui/sheet'
import { Switch } from '@/components/ui/switch'
import { ChipRow, DateRange, FacetGroup, SearchField } from '@/components/filters'
import { seriesColor } from '@/components/series'
import { StatLabel } from '@/components/stat'
import { DisclosurePanel } from '@/components/states'
import { COST_STATE_META, OUTCOME_META } from '@/components/status'
import type { CostState, OutcomeLabel } from '@/api'
import {
  CLIENTS,
  ERROR_COUNT,
  FACET_COUNTS,
  OUTCOME_COUNTS,
  MODELS,
  PROJECTS,
  RANGE_PRESETS,
  SAVED_VIEWS,
  SOURCES,
  TODAY,
  TRACED_COUNT,
} from './data'

const STATES: CostState[] = ['priced', 'free', 'unpriced', 'unavailable']

const OUTCOMES: OutcomeLabel[] = ['successful', 'partial', 'failed', 'abandoned', 'unrated']

export interface FilterState {
  search: string
  savedView: string | null
  range: string
  since: string | null
  until: string | null
  states: string[]
  outcomes: string[]
  traced: boolean | null
  hasErrors: boolean | null
  clients: string[]
  models: string[]
  projects: string[]
  includeSidechains: boolean
}

export const INITIAL_FILTERS: FilterState = {
  search: '',
  savedView: 'all',
  range: '30',
  since: '2026-08-10',
  until: TODAY,
  states: [],
  outcomes: [],
  traced: null,
  hasErrors: null,
  clients: [],
  models: [],
  projects: [],
  includeSidechains: true,
}

export function isDirty(filters: FilterState): boolean {
  return (
    filters.search !== '' ||
    filters.states.length > 0 ||
    filters.outcomes.length > 0 ||
    filters.traced !== null ||
    filters.hasErrors !== null ||
    filters.clients.length > 0 ||
    filters.models.length > 0 ||
    filters.projects.length > 0 ||
    !filters.includeSidechains
  )
}

function toggle(list: string[], value: string): string[] {
  return list.includes(value) ? list.filter((item) => item !== value) : [...list, value]
}

export function RailContent({
  filters,
  onChange,
  onReset,
}: {
  filters: FilterState
  onChange: (patch: Partial<FilterState>) => void
  onReset: () => void
}) {
  const undetected = SOURCES.filter((source) => !source.detected)

  return (
    <div className="flex flex-col gap-6">
      <SearchField
        value={filters.search}
        onChange={(search) => onChange({ search })}
        placeholder="Search sessions, models, repos"
      />

      <div className="space-y-2">
        <StatLabel>Saved views</StatLabel>
        <ChipRow
          options={SAVED_VIEWS}
          active={filters.savedView}
          onSelect={(savedView) => onChange({ savedView })}
        />
      </div>

      <div className="space-y-2">
        <StatLabel>Range</StatLabel>
        <ChipRow
          options={RANGE_PRESETS}
          active={filters.range}
          onSelect={(range) => onChange({ range })}
        />
        <DateRange
          since={filters.since}
          until={filters.until}
          max={TODAY}
          onChange={(patch) => onChange(patch)}
        />
      </div>

      <Separator />

      <FacetGroup
        title="Cost state"
        options={STATES.map((state) => ({
          value: state,
          label: state,
          count: FACET_COUNTS.states[state],
          color: COST_STATE_META[state].color,
        }))}
        selected={filters.states}
        onToggle={(value) => onChange({ states: toggle(filters.states, value) })}
      />

      <FacetGroup
        title="Outcome"
        options={OUTCOMES.map((outcome) => ({
          value: outcome,
          label: outcome,
          count: OUTCOME_COUNTS[outcome],
          color: OUTCOME_META[outcome].color,
        }))}
        selected={filters.outcomes}
        onToggle={(value) => onChange({ outcomes: toggle(filters.outcomes, value) })}
      />

      <div className="space-y-2">
        <StatLabel>Trace</StatLabel>
        <ChipRow
          options={[
            { value: 'traced', label: `Traced (${TRACED_COUNT})` },
            { value: 'errors', label: `Has errors (${ERROR_COUNT})` },
          ]}
          active={filters.traced ? 'traced' : filters.hasErrors ? 'errors' : null}
          onSelect={(value) =>
            value === 'traced'
              ? onChange({ traced: filters.traced ? null : true, hasErrors: null })
              : onChange({ hasErrors: filters.hasErrors ? null : true, traced: null })
          }
        />
      </div>

      <FacetGroup
        title="Clients"
        options={CLIENTS.map((client, index) => ({
          value: client.id,
          label: client.label,
          count: FACET_COUNTS.clients[client.id],
          color: seriesColor(index),
        }))}
        selected={filters.clients}
        onToggle={(value) => onChange({ clients: toggle(filters.clients, value) })}
      />

      <div className="max-h-52 overflow-y-auto scroll-thin">
        <FacetGroup
          title="Models"
          options={MODELS.map((model) => ({
            value: model.key,
            label: model.label,
            count: FACET_COUNTS.models[model.key],
          }))}
          selected={filters.models}
          onToggle={(value) => onChange({ models: toggle(filters.models, value) })}
        />
      </div>

      <div className="max-h-52 overflow-y-auto scroll-thin">
        <FacetGroup
          title="Projects"
          options={PROJECTS.map((project) => ({
            value: project.key,
            label: project.label,
            count: FACET_COUNTS.projects[project.key],
          }))}
          selected={filters.projects}
          onToggle={(value) => onChange({ projects: toggle(filters.projects, value) })}
        />
      </div>

      <div className="flex items-center gap-2.5 rounded-md border bg-card p-2.5">
        <Switch
          id="rail-sidechains"
          checked={filters.includeSidechains}
          onCheckedChange={(includeSidechains) => onChange({ includeSidechains })}
        />
        <Label htmlFor="rail-sidechains" className="font-normal">
          Include subagent requests
        </Label>
      </div>

      {isDirty(filters) ? (
        <Button variant="outline" size="sm" onClick={onReset} className="w-full">
          Clear all filters
        </Button>
      ) : null}

      {undetected.length > 0 ? (
        <DisclosurePanel
          title="Not detected here"
          summary={`${undetected.length} sources ship with the tool and found nothing on this machine`}
        >
          <div className="space-y-2">
            {undetected.map((source) => (
              <div key={source.id} className="rounded-md border border-dashed p-2.5">
                <div className="text-xs text-muted-foreground">{source.label}</div>
                <div className="tabular mt-1 text-[10px] break-all text-muted-foreground">
                  {source.path}
                </div>
              </div>
            ))}
            <p className="text-[11px] leading-relaxed text-muted-foreground">
              Not installed here, so they are kept out of every filter and total. Point one at a log
              path to bring it in.
            </p>
          </div>
        </DisclosurePanel>
      ) : null}
    </div>
  )
}

export function FilterRail({
  filters,
  onChange,
  onReset,
  open,
  onOpenChange,
}: {
  filters: FilterState
  onChange: (patch: Partial<FilterState>) => void
  onReset: () => void
  open: boolean
  onOpenChange: (open: boolean) => void
}) {
  return (
    <>
      <aside className="hidden w-[276px] shrink-0 self-stretch border-r bg-muted/40 p-4 lg:block">
        <RailContent filters={filters} onChange={onChange} onReset={onReset} />
      </aside>

      <Sheet open={open} onOpenChange={onOpenChange}>
        <SheetContent side="left" className="w-[300px] gap-0 p-0">
          <SheetHeader>
            <SheetTitle>Filters</SheetTitle>
          </SheetHeader>
          <div className="scroll-thin overflow-y-auto p-4">
            <RailContent filters={filters} onChange={onChange} onReset={onReset} />
          </div>
        </SheetContent>
      </Sheet>
    </>
  )
}
