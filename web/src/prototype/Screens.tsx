import { useState } from 'react'

import { Separator } from '@/components/ui/separator'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet'
import { CodeBlock, MetaGrid, PathList, Section } from '@/components/detail'
import { FilterChips, type ActiveFilter } from '@/components/filters'
import { TOKEN_BUCKETS } from '@/components/series'
import { EmptyState } from '@/components/states'
import { BucketBar, CostStateBadge, OutcomeBadge } from '@/components/status'
import { CapabilityGrid, ContextOccupancy, InsightList, SpanTimeline } from '@/components/trace'
import {
  formatClock,
  formatCount,
  formatDuration,
  formatMoney,
  formatPercent,
  formatTokens,
} from '@/format'
import { OverviewScreen } from './OverviewScreen'
import { PricingScreen } from './PricingScreen'
import { SessionsScreen } from './SessionsScreen'
import { SourcesScreen } from './SourcesScreen'
import { FilterRail, INITIAL_FILTERS, isDirty, type FilterState } from './Rail'
import {
  CAPABILITIES,
  CLIENTS,
  CONTEXT_SNAPSHOTS,
  PROJECTS,
  TOTALS,
  TRACE_INSIGHTS,
  TRACE_SPANS,
  type PrototypeSession,
} from './data'

export type ScreenId = 'overview' | 'sessions' | 'sources' | 'pricing'

export const SCREEN_LABELS: Record<ScreenId, string> = {
  overview: 'Overview',
  sessions: 'Sessions',
  sources: 'Sources',
  pricing: 'Models and pricing',
}

const BUCKET_WEIGHT: Record<string, number> = {
  uncached_input: 1,
  cache_read: 0.1,
  cache_write: 1.25,
  output: 5,
}

function bucketCosts(session: PrototypeSession): Record<string, number> {
  if (!session.tokens || session.cost === null) return {}
  const weighted = TOKEN_BUCKETS.map(
    (bucket) => session.tokens![bucket.key] * BUCKET_WEIGHT[bucket.key],
  )
  const total = weighted.reduce((a, b) => a + b, 0)
  return Object.fromEntries(
    TOKEN_BUCKETS.map((bucket, index) => [
      bucket.key,
      total > 0 ? (weighted[index] / total) * session.cost! : 0,
    ]),
  )
}

function costNote(session: PrototypeSession): string {
  switch (session.state) {
    case 'priced':
      return `${formatCount(session.requests)} requests priced from the rate table at list prices.`
    case 'free':
      return 'A local runtime, so the provider is marked free and this counts at zero.'
    case 'unpriced':
      return 'Tokens are counted, no rate entry matches this model, so cost stays out of totals.'
    case 'unavailable':
      return 'This client logs no token counts, so cost is left blank instead of guessed.'
  }
}

function SessionDrawer({
  session,
  onClose,
}: {
  session: PrototypeSession | null
  onClose: () => void
}) {
  const perBucket = session ? bucketCosts(session) : {}

  return (
    <Sheet open={session !== null} onOpenChange={(open) => (open ? null : onClose())}>
      <SheetContent className="w-full gap-0 p-0 sm:max-w-md">
        {session ? (
          <>
            <SheetHeader className="gap-1.5">
              <p className="text-[11px] font-medium uppercase tracking-[0.08em] text-primary">
                Session
              </p>
              <SheetTitle className="tabular text-base">{session.id}</SheetTitle>
              <SheetDescription>
                {session.client} &middot; {session.models[0]} &middot; {session.startedLabel}
              </SheetDescription>
            </SheetHeader>
            <Separator />

            <div className="scroll-thin flex flex-col gap-6 overflow-y-auto p-card">
              <Section
                title="Cost"
                action={
                  <div className="flex gap-1.5">
                    <CostStateBadge state={session.state} />
                    <OutcomeBadge outcome={session.outcome} />
                  </div>
                }
              >
                <p className="tabular text-3xl font-semibold leading-none">
                  {session.cost === null ? 'not available' : formatMoney(session.cost)}
                </p>
                <p className="text-xs leading-relaxed text-muted-foreground">{costNote(session)}</p>
              </Section>

              {session.tokens ? (
                <Section title="Token buckets">
                  <BucketBar
                    formatValue={formatTokens}
                    segments={TOKEN_BUCKETS.map((bucket) => ({
                      key: bucket.key,
                      label: bucket.label,
                      value: session.tokens ? session.tokens[bucket.key] : 0,
                      color: bucket.color,
                    }))}
                  />
                  <div>
                    {TOKEN_BUCKETS.map((bucket) => (
                      <div
                        key={bucket.key}
                        className="grid grid-cols-[14px_1fr_auto_auto] items-center gap-2 border-b py-2 last:border-b-0"
                      >
                        <span
                          aria-hidden
                          className="size-2 rounded-full"
                          style={{ background: bucket.color }}
                        />
                        <span className="text-xs">{bucket.label}</span>
                        <span className="tabular text-xs text-muted-foreground">
                          {formatTokens(session.tokens ? session.tokens[bucket.key] : 0)}
                        </span>
                        <span className="tabular w-16 text-right text-xs font-medium">
                          {session.cost === null ? 'n/a' : formatMoney(perBucket[bucket.key] ?? 0)}
                        </span>
                      </div>
                    ))}
                  </div>
                  {session.reasoning > 0 ? (
                    <p className="text-xs text-muted-foreground">
                      Reasoning &mdash; {formatTokens(session.reasoning)}, inside the{' '}
                      {formatTokens(session.tokens.output)} output above.
                    </p>
                  ) : null}
                </Section>
              ) : (
                <EmptyState
                  title="This client logs no token counts"
                  description="The session, its requests and its timing are real and counted. Tokens and cost are left blank rather than guessed."
                />
              )}

              {session.traced ? (
                <>
                  <Section
                    title="Context window"
                    action={
                      <span className="tabular text-[11px] text-muted-foreground">
                        {CONTEXT_SNAPSHOTS.length} model calls
                      </span>
                    }
                  >
                    <ContextOccupancy
                      points={CONTEXT_SNAPSHOTS}
                      formatPercent={formatPercent}
                      formatTokens={formatTokens}
                      formatClock={formatClock}
                    />
                    <p className="text-xs leading-relaxed text-muted-foreground">
                      Each bar is one model call. Amber is above 85% of the window; the violet tick
                      marks a compaction. Gaps are calls where the client logged no capacity, so
                      occupancy is left unknown rather than assumed.
                    </p>
                  </Section>

                  <Section title="Trace">
                    <SpanTimeline
                      spans={TRACE_SPANS.map((span) => ({
                        spanId: span.spanId,
                        kind: span.kind,
                        name: span.name,
                        status: span.status,
                        depth: span.depth,
                        duration: span.durationMs === null ? null : formatDuration(span.durationMs),
                        tokens: span.tokens === null ? null : formatTokens(span.tokens),
                      }))}
                    />
                  </Section>

                  <Section title="Insights">
                    <InsightList insights={TRACE_INSIGHTS} />
                  </Section>

                  <Section title="What can be known here">
                    <CapabilityGrid capabilities={CAPABILITIES} />
                  </Section>
                </>
              ) : (
                <Section title="Trace">
                  <p className="text-xs leading-relaxed text-muted-foreground">
                    This session was recorded before span capture, or by a client that does not log
                    turn structure. Its totals are still real; the per-turn breakdown simply is not
                    there to show.
                  </p>
                </Section>
              )}

              <Section title="Where it came from">
                <MetaGrid
                  items={[
                    { label: 'Client', value: session.client },
                    { label: 'Provider', value: session.provider },
                    { label: 'Models', value: session.models.join(', ') },
                    { label: 'Project', value: session.project },
                    {
                      label: 'Working directory',
                      value: session.workingDirectory ?? 'none recorded',
                    },
                    { label: 'Repository', value: session.repository ?? 'none' },
                    { label: 'Branch', value: session.branch ?? 'none' },
                    { label: 'Requests', value: formatCount(session.requests) },
                    { label: 'Log span', value: session.duration },
                    { label: 'Subagent thread', value: session.sidechain ? 'yes' : 'no' },
                    { label: 'Errors', value: String(session.errorCount) },
                    { label: 'Provenance', value: session.provenance },
                    { label: 'Machine', value: session.machine },
                  ]}
                />
              </Section>

              <Section title="Raw log files">
                <PathList paths={session.rawSource} />
              </Section>

              <Section title="Reprice this model">
                <CodeBlock>
                  {`{"match": "${session.models[0].toLowerCase().replace(/\s+/g, '-')}", "input": 0, "output": 0}`}
                </CodeBlock>
              </Section>
            </div>
          </>
        ) : null}
      </SheetContent>
    </Sheet>
  )
}

export function Screens({
  screen,
  onSelectScreen,
  railOpen,
  onRailOpenChange,
}: {
  screen: ScreenId
  onSelectScreen: (screen: ScreenId) => void
  railOpen: boolean
  onRailOpenChange: (open: boolean) => void
}) {
  const [filters, setFilters] = useState<FilterState>(INITIAL_FILTERS)
  const [active, setActive] = useState<PrototypeSession | null>(null)

  const patch = (next: Partial<FilterState>) => setFilters((current) => ({ ...current, ...next }))
  const reset = () => setFilters(INITIAL_FILTERS)

  const chips: ActiveFilter[] = [
    ...filters.states.map((value) => ({
      key: `state:${value}`,
      group: 'state',
      label: value,
      onRemove: () => patch({ states: filters.states.filter((item) => item !== value) }),
    })),
    ...filters.outcomes.map((value) => ({
      key: `outcome:${value}`,
      group: 'outcome',
      label: value,
      onRemove: () => patch({ outcomes: filters.outcomes.filter((item) => item !== value) }),
    })),
    ...(filters.traced
      ? [{ key: 'traced', group: 'trace', label: 'traced only', onRemove: () => patch({ traced: null }) }]
      : []),
    ...(filters.hasErrors
      ? [{ key: 'errors', group: 'trace', label: 'has errors', onRemove: () => patch({ hasErrors: null }) }]
      : []),
    ...filters.clients.map((value) => ({
      key: `client:${value}`,
      group: 'client',
      label: CLIENTS.find((client) => client.id === value)?.label ?? value,
      onRemove: () => patch({ clients: filters.clients.filter((item) => item !== value) }),
    })),
    ...filters.models.map((value) => ({
      key: `model:${value}`,
      group: 'model',
      label: value,
      onRemove: () => patch({ models: filters.models.filter((item) => item !== value) }),
    })),
    ...filters.projects.map((value) => ({
      key: `project:${value}`,
      group: 'project',
      label: PROJECTS.find((project) => project.key === value)?.label ?? value,
      onRemove: () => patch({ projects: filters.projects.filter((item) => item !== value) }),
    })),
    ...(filters.search
      ? [
          {
            key: 'search',
            group: 'search',
            label: filters.search,
            onRemove: () => patch({ search: '' }),
          },
        ]
      : []),
    ...(filters.includeSidechains
      ? []
      : [
          {
            key: 'threads',
            group: 'threads',
            label: 'main thread only',
            onRemove: () => patch({ includeSidechains: true }),
          },
        ]),
  ]

  return (
    <div className="flex flex-1 items-start">
      <FilterRail
        filters={filters}
        onChange={patch}
        onReset={reset}
        open={railOpen}
        onOpenChange={onRailOpenChange}
      />

      <main className="min-w-0 flex-1 space-y-3 p-4 lg:p-6">
        <div className="flex flex-wrap items-center gap-2">
          <span className="tabular text-xs text-muted-foreground">
            {formatCount(TOTALS.sessions)} sessions &middot; {formatCount(TOTALS.requests)} requests
          </span>
          <FilterChips filters={chips} onClear={isDirty(filters) ? reset : undefined} />
        </div>

        {screen === 'overview' ? (
          <OverviewScreen onSeeSources={() => onSelectScreen('sources')} />
        ) : screen === 'sessions' ? (
          <SessionsScreen onOpen={setActive} />
        ) : screen === 'sources' ? (
          <SourcesScreen />
        ) : (
          <PricingScreen />
        )}

        <p className="pt-2 text-center text-xs text-muted-foreground">
          List prices as of {TOTALS.ratesAsOf} &middot; nothing left this machine.
        </p>
      </main>

      <SessionDrawer session={active} onClose={() => setActive(null)} />
    </div>
  )
}
