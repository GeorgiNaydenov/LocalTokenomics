import { useState } from 'react'
import { DownloadIcon, RefreshCwIcon, TrashIcon } from 'lucide-react'
import { toast } from 'sonner'

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Progress } from '@/components/ui/progress'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'
import { Skeleton } from '@/components/ui/skeleton'
import { Switch } from '@/components/ui/switch'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import { Panel, PanelBody, PanelHeader, PanelNote } from '@/components/panel'
import { Stat, StatGrid, StatLabel } from '@/components/stat'
import {
  BucketBar,
  ComparisonMeter,
  CostStateBadge,
  Legend,
  Meter,
  MeterRow,
  OutcomeBadge,
  ProvenanceBadge,
} from '@/components/status'
import { CapabilityGrid, ContextOccupancy, InsightList, SpanTimeline } from '@/components/trace'
import {
  DisclosurePanel,
  EmptyState,
  PanelSkeleton,
  SortButton,
  StatSkeleton,
  WarningsList,
} from '@/components/states'
import {
  ChipRow,
  DateRange,
  FacetGroup,
  FilterChips,
  SearchField,
  SortSelect,
} from '@/components/filters'
import { CodeBlock, MetaGrid, PathList } from '@/components/detail'
import { SessionCard, TokenCell } from '@/components/session'
import { SourceCard } from '@/components/source-card'
import { Sparkline } from '@/components/sparkline'
import { formatClock, formatCount, formatDuration, formatMoney, formatPercent, formatTokens } from '@/format'
import {
  CAPABILITIES,
  CONTEXT_SNAPSHOTS,
  RANGE_PRESETS,
  SCAN_WARNINGS,
  SORT_OPTIONS,
  TRACE_INSIGHTS,
  TRACE_SPANS,
} from './data'

const SURFACE_TOKENS = [
  'background',
  'foreground',
  'card',
  'popover',
  'primary',
  'secondary',
  'muted',
  'accent',
  'border',
  'input',
  'ring',
]

const SEMANTIC_TOKENS = ['destructive', 'success', 'warning']

const CHART_TOKENS = [
  'chart-1',
  'chart-2',
  'chart-3',
  'chart-4',
  'chart-5',
  'chart-6',
  'chart-7',
  'chart-8',
  'chart-other',
]

const TYPE_SCALE = [
  { name: 'Hero numeral', className: 'text-[2.5rem] font-semibold tabular tracking-[-0.02em]' },
  { name: 'Stat numeral', className: 'text-2xl font-semibold tabular' },
  { name: 'Panel title', className: 'text-[0.9375rem] font-semibold tracking-[-0.01em]' },
  { name: 'Body / UI', className: 'text-sm' },
  { name: 'Hint', className: 'text-xs text-muted-foreground' },
  { name: 'Label', className: 'text-[11px] font-medium uppercase tracking-[0.08em] text-muted-foreground' },
]

function Swatch({ token }: { token: string }) {
  return (
    <div className="space-y-1.5">
      <div className="h-12 rounded-md border" style={{ background: `var(--${token})` }} />
      <p className="tabular text-[11px] text-muted-foreground">--{token}</p>
    </div>
  )
}

function Row({ title, hint, children }: { title: string; hint?: string; children: React.ReactNode }) {
  return (
    <div className="grid gap-3 border-b py-6 last:border-b-0 lg:grid-cols-[220px_1fr] lg:gap-8">
      <div className="space-y-1">
        <h3 className="text-sm font-medium">{title}</h3>
        {hint ? <p className="text-xs leading-relaxed text-muted-foreground">{hint}</p> : null}
      </div>
      <div className="min-w-0 space-y-4">{children}</div>
    </div>
  )
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <Panel>
      <PanelHeader title={title} />
      <PanelBody className="py-0">{children}</PanelBody>
    </Panel>
  )
}

const TREND = [4, 9, 6, 14, 11, 3, 2, 17, 21, 15, 24, 19, 6, 4, 26, 22, 30, 25, 18, 7, 5, 28, 33, 27, 31, 24, 9, 6, 35, 29]

export function Gallery() {
  const [checked, setChecked] = useState(true)
  const [switched, setSwitched] = useState(true)
  const [search, setSearch] = useState('')
  const [facets, setFacets] = useState<string[]>(['priced'])
  const [stack, setStack] = useState('model')
  const [sortActive, setSortActive] = useState(true)
  const [range, setRange] = useState('30')
  const [sort, setSort] = useState('cost:desc')

  return (
    <div className="mx-auto max-w-5xl space-y-3 p-4 lg:p-6">
      <Section title="Colour tokens">
        <Row title="Surfaces and ink" hint="Every token is defined in both themes. Flip the theme in the header — nothing here is hard-coded.">
          <div className="grid grid-cols-3 gap-3 sm:grid-cols-6">
            {SURFACE_TOKENS.map((token) => (
              <Swatch key={token} token={token} />
            ))}
          </div>
        </Row>
        <Row title="Semantic" hint="Reserved meanings. Never used decoratively.">
          <div className="grid grid-cols-3 gap-3 sm:grid-cols-6">
            {SEMANTIC_TOKENS.map((token) => (
              <Swatch key={token} token={token} />
            ))}
          </div>
        </Row>
        <Row
          title="Chart series"
          hint="Eight slots in fixed order. A series keeps its slot everywhere, so filtering never repaints a surviving series."
        >
          <div className="grid grid-cols-3 gap-3 sm:grid-cols-9">
            {CHART_TOKENS.map((token) => (
              <Swatch key={token} token={token} />
            ))}
          </div>
        </Row>
        <Row title="Cost state" hint="unavailable is deliberately colourless — no tokens were logged, so no cost is implied.">
          <div className="flex flex-wrap gap-2">
            <CostStateBadge state="priced" />
            <CostStateBadge state="free" />
            <CostStateBadge state="unpriced" />
            <CostStateBadge state="unavailable" />
          </div>
        </Row>
        <Row title="Outcome" hint="How the session ended. unrated is never guessed at.">
          <div className="flex flex-wrap gap-2">
            <OutcomeBadge outcome="successful" />
            <OutcomeBadge outcome="partial" />
            <OutcomeBadge outcome="failed" />
            <OutcomeBadge outcome="abandoned" />
            <OutcomeBadge outcome="unrated" />
          </div>
        </Row>
        <Row title="Provenance" hint="How a number was arrived at.">
          <div className="flex flex-wrap gap-2">
            <ProvenanceBadge provenance="measured" />
            <ProvenanceBadge provenance="derived" />
            <ProvenanceBadge provenance="estimated" />
            <ProvenanceBadge provenance="inferred" />
            <ProvenanceBadge provenance="unavailable" />
          </div>
        </Row>
      </Section>

      <Section title="Typography">
        <Row title="Scale" hint="Inter for text, Geist Mono for every numeral. Numerals are tabular so columns align.">
          <div className="space-y-3">
            {TYPE_SCALE.map((step) => (
              <div key={step.name} className="flex flex-wrap items-baseline gap-4">
                <span className="w-28 shrink-0 text-[11px] text-muted-foreground">{step.name}</span>
                <span className={step.className}>
                  {step.className.includes('tabular') ? '$3,431.96' : 'API-equivalent cost'}
                </span>
              </div>
            ))}
          </div>
        </Row>
        <Row title="Density" hint="The comfortable scale: 14px base, 36px controls, 44px rows, 24px card padding.">
          <div className="tabular grid grid-cols-2 gap-3 text-xs text-muted-foreground sm:grid-cols-4">
            <div className="rounded-md border p-3">--text-ui · 14px</div>
            <div className="rounded-md border p-3">--control-height · 36px</div>
            <div className="rounded-md border p-3">--row-height · 44px</div>
            <div className="rounded-md border p-3">--card-padding · 24px</div>
          </div>
        </Row>
      </Section>

      <Section title="Actions">
        <Row title="Button variants">
          <div className="flex flex-wrap items-center gap-2">
            <Button>Rescan logs</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="destructive">
              <TrashIcon /> Rebuild store
            </Button>
            <Button variant="link">Link</Button>
          </div>
        </Row>
        <Row title="Sizes and state">
          <div className="flex flex-wrap items-center gap-2">
            <Button size="sm">
              <RefreshCwIcon /> Small
            </Button>
            <Button size="default">Default</Button>
            <Button size="lg">Large</Button>
            <Button size="icon" aria-label="Export">
              <DownloadIcon />
            </Button>
            <Button disabled>Disabled</Button>
            <Button onClick={() => toast.success('Rescan complete', { description: '412 files, 3 changed.' })}>
              Fire a toast
            </Button>
          </div>
        </Row>
        <Row title="Segmented control" hint="Toggle group — used for chart stacking and metric switches.">
          <ToggleGroup
            type="single"
            variant="outline"
            value={stack}
            onValueChange={(value) => value && setStack(value)}
          >
            <ToggleGroupItem value="client">Client</ToggleGroupItem>
            <ToggleGroupItem value="provider">Provider</ToggleGroupItem>
            <ToggleGroupItem value="model">Model</ToggleGroupItem>
          </ToggleGroup>
        </Row>
        <Row title="Overlays">
          <div className="flex flex-wrap items-center gap-2">
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline">Open dialog</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Rebuild the local store?</DialogTitle>
                  <DialogDescription>
                    This discards ~/.ai-usage-cost/usage.db and reparses every log from scratch.
                    Nothing is uploaded and no source file is modified.
                  </DialogDescription>
                </DialogHeader>
                <DialogFooter>
                  <Button variant="outline">Cancel</Button>
                  <Button variant="destructive">Rebuild</Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>

            <Popover>
              <PopoverTrigger asChild>
                <Button variant="outline">Popover</Button>
              </PopoverTrigger>
              <PopoverContent className="space-y-2">
                <StatLabel>Date range</StatLabel>
                <div className="grid grid-cols-2 gap-2">
                  <Input type="date" defaultValue="2026-08-10" />
                  <Input type="date" defaultValue="2026-09-08" />
                </div>
              </PopoverContent>
            </Popover>

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline">Dropdown</Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="start">
                <DropdownMenuItem>Export report.json</DropdownMenuItem>
                <DropdownMenuItem>Export report.png</DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem variant="destructive">Rebuild store</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="outline">Tooltip</Button>
              </TooltipTrigger>
              <TooltipContent>Cache reads bill at 0.1× the input price</TooltipContent>
            </Tooltip>
          </div>
        </Row>
      </Section>

      <Section title="Inputs">
        <Row title="Text and search">
          <div className="grid gap-3 sm:grid-cols-2">
            <div className="space-y-1.5">
              <Label htmlFor="g-model">Model prefix</Label>
              <Input id="g-model" placeholder="claude-opus" />
            </div>
            <div className="space-y-1.5">
              <Label>Search</Label>
              <SearchField value={search} onChange={setSearch} placeholder="Search sessions" />
            </div>
          </div>
        </Row>
        <Row title="Select">
          <Select defaultValue="cost">
            <SelectTrigger className="w-56">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="cost">Sort by cost</SelectItem>
              <SelectItem value="tokens">Sort by tokens</SelectItem>
              <SelectItem value="started">Sort by start time</SelectItem>
            </SelectContent>
          </Select>
        </Row>
        <Row title="Toggles">
          <div className="flex flex-wrap items-center gap-6">
            <div className="flex items-center gap-2">
              <Checkbox
                id="g-check"
                checked={checked}
                onCheckedChange={(value) => setChecked(value === true)}
              />
              <Label htmlFor="g-check" className="font-normal">
                Include sidechains
              </Label>
            </div>
            <div className="flex items-center gap-2">
              <Switch id="g-switch" checked={switched} onCheckedChange={setSwitched} />
              <Label htmlFor="g-switch" className="font-normal">
                Auto-rescan every 5 minutes
              </Label>
            </div>
          </div>
        </Row>
        <Row title="Facets and chips" hint="The filter rail's vocabulary.">
          <div className="grid gap-6 sm:grid-cols-2">
            <FacetGroup
              title="Cost state"
              options={[
                { value: 'priced', label: 'Priced', count: 34118 },
                { value: 'free', label: 'Free', count: 1604 },
                { value: 'unpriced', label: 'Unpriced', count: 1072 },
                { value: 'unavailable', label: 'Unavailable', count: 3400 },
              ]}
              selected={facets}
              onToggle={(value) =>
                setFacets((list) =>
                  list.includes(value) ? list.filter((item) => item !== value) : [...list, value],
                )
              }
            />
            <div className="space-y-3">
              <StatLabel>Active filters</StatLabel>
              <FilterChips
                filters={facets.map((value) => ({
                  key: value,
                  group: 'state',
                  label: value,
                  onRemove: () => setFacets((list) => list.filter((item) => item !== value)),
                }))}
                onClear={() => setFacets([])}
              />
            </div>
          </div>
        </Row>
      </Section>

      <Section title="Data display">
        <Row title="Stat tiles" hint="Values count up on mount and hold still under prefers-reduced-motion.">
          <StatGrid className="xl:grid-cols-2">
            <Stat
              label="API-equivalent cost"
              value={3431.96}
              format={formatMoney}
              emphasis="hero"
              hint="List prices for the tokens actually spent."
            />
            <Stat label="Tokens" value={411882004} format={formatTokens} hint="Across 40,194 requests." />
          </StatGrid>
        </Row>
        <Row title="Meters and bars">
          <div className="space-y-4">
            <Meter value={0.79} label="Cache hit share" />
            <Meter value={0.31} color="var(--success)" label="Free share" />
            <BucketBar
              segments={[
                { key: 'a', label: 'Uncached input', value: 9, color: 'var(--bucket-uncached-input)' },
                { key: 'b', label: 'Cache read', value: 78, color: 'var(--bucket-cache-read)' },
                { key: 'c', label: 'Cache write', value: 9, color: 'var(--bucket-cache-write)' },
                { key: 'd', label: 'Output', value: 4, color: 'var(--bucket-output)' },
              ]}
            />
            <Legend
              items={[
                { key: 'a', label: 'Uncached input', color: 'var(--bucket-uncached-input)', value: '9%' },
                { key: 'b', label: 'Cache read', color: 'var(--bucket-cache-read)', value: '78%' },
                { key: 'c', label: 'Cache write', color: 'var(--bucket-cache-write)', value: '9%' },
                { key: 'd', label: 'Output', color: 'var(--bucket-output)', value: '4%' },
              ]}
            />
            <Progress value={64} />
          </div>
        </Row>
        <Row title="Sortable header">
          <div className="flex gap-6">
            <SortButton label="Cost" active={sortActive} direction="desc" onClick={() => setSortActive(true)} />
            <SortButton label="Tokens" active={!sortActive} direction="asc" onClick={() => setSortActive(false)} />
          </div>
        </Row>
        <Row title="Badges">
          <div className="flex flex-wrap gap-2">
            <Badge>Default</Badge>
            <Badge variant="secondary">Secondary</Badge>
            <Badge variant="outline">Outline</Badge>
            <Badge variant="destructive">Destructive</Badge>
            <Badge variant="ghost">Ghost</Badge>
          </div>
        </Row>
      </Section>

      <Section title="Feedback and structure">
        <Row title="Alert">
          <Alert>
            <AlertTitle>3 models had no matching rate</AlertTitle>
            <AlertDescription>
              Their tokens are listed but excluded from cost totals until you add a price to
              rates.json. A model is never silently priced at zero.
            </AlertDescription>
          </Alert>
        </Row>
        <Row title="Empty state">
          <EmptyState
            title="No sessions match these filters"
            description="Nothing was lost — the local store still holds every scanned request."
            action={<Button variant="outline" size="sm">Clear all filters</Button>}
          />
        </Row>
        <Row title="Loading" hint="Skeletons mirror the shape of what is arriving, not a generic spinner.">
          <div className="grid gap-3 sm:grid-cols-2">
            <StatSkeleton />
            <PanelSkeleton rows={3} />
          </div>
        </Row>
        <Row title="Tabs">
          <Tabs defaultValue="overview">
            <TabsList>
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="sessions">Sessions</TabsTrigger>
              <TabsTrigger value="sources">Sources</TabsTrigger>
            </TabsList>
            <TabsContent value="overview" className="pt-3 text-xs text-muted-foreground">
              Totals, trends and breakdowns for the current slice.
            </TabsContent>
            <TabsContent value="sessions" className="pt-3 text-xs text-muted-foreground">
              Every session, sortable and inspectable.
            </TabsContent>
            <TabsContent value="sources" className="pt-3 text-xs text-muted-foreground">
              Which logs were found and what they carry.
            </TabsContent>
          </Tabs>
        </Row>
        <Row title="Accordion">
          <Accordion type="single" collapsible>
            <AccordionItem value="a">
              <AccordionTrigger>How is cost worked out?</AccordionTrigger>
              <AccordionContent>
                Tokens are normalised into four disjoint billable buckets and priced from
                rates.json. Cache and batch multipliers apply to the model's base input price.
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="b">
              <AccordionTrigger>Why is a session showing no cost?</AccordionTrigger>
              <AccordionContent>
                Its client logged the session but no token counts. The request is still counted;
                cost is never fabricated.
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </Row>
        <Row title="Separator and skeleton primitives">
          <div className="space-y-3">
            <Skeleton className="h-4 w-2/3" />
            <Separator />
            <p className="tabular text-xs text-muted-foreground">
              {formatCount(40194)} requests · {formatTokens(411882004)} tokens
            </p>
          </div>
        </Row>
      </Section>

      <Section title="Domain components">
        <Row title="Sparkline" hint="Plain SVG, not a chart library — several render per screen in KPI tiles and source cards.">
          <div className="flex flex-wrap items-end gap-8">
            <Sparkline values={TREND} width={120} height={26} />
            <Sparkline values={TREND} width={120} height={26} color="var(--primary)" fill />
            <Sparkline values={TREND} width={240} height={34} color="var(--chart-2)" fill />
          </div>
        </Row>
        <Row title="Meter row" hint="Ranked breakdowns: cost by model, by project, provider multipliers. Free and unpriced rows keep their place.">
          <div>
            <MeterRow label="Claude Opus 5" meta="402 sessions" value={formatMoney(1489.22)} share="43%" fraction={0.92} color="var(--chart-1)" />
            <MeterRow label="Claude Sonnet 5" meta="318 sessions" value={formatMoney(812.4)} share="24%" fraction={0.5} color="var(--chart-2)" />
            <MeterRow label="Grok 4" meta="24 sessions · unpriced" value="n/a" share="unpriced" fraction={0} color="var(--state-unpriced)" />
          </div>
        </Row>
        <Row title="Comparison meters" hint="Two lengths against one scale — what caching saved.">
          <div className="space-y-3">
            <ComparisonMeter caption="Same tokens billed with no cache discount" value={formatMoney(16316.27)} fraction={1} color="var(--muted-foreground)" />
            <ComparisonMeter caption="Actually billed at cache rates" value={formatMoney(3431.96)} fraction={0.21} />
          </div>
        </Row>
        <Row title="Token cell" hint="Sits in the sessions table: the number plus a bar coloured by the row's cost state.">
          <div className="flex flex-col items-end gap-2">
            <TokenCell label={formatTokens(12884003)} fraction={1} state="priced" />
            <TokenCell label={formatTokens(4118770)} fraction={0.32} state="free" />
            <TokenCell label={null} fraction={0} state="unavailable" />
          </div>
        </Row>
        <Row title="Source card" hint="One reader found on this machine, with its own activity trend.">
          <div className="grid gap-0 rounded-md border sm:grid-cols-2">
            <SourceCard source={{ id: 'a', label: 'Claude Code', path: '~/.claude/projects/*/*.jsonl', hasTokens: true, color: 'var(--chart-1)', headline: formatMoney(2430.56), foot: '816 sessions logged', trend: TREND }} />
            <SourceCard source={{ id: 'b', label: 'Jan', path: '~/jan/threads', hasTokens: false, color: 'var(--chart-6)', headline: formatCount(613), foot: 'requests logged, no token counts', trend: TREND.slice(0, 14) }} />
          </div>
        </Row>
        <Row title="Session card" hint="The phone layout for the sessions table.">
          <div className="max-w-sm">
            <SessionCard
              session={{ id: '9f3c1a44', state: 'priced', model: 'Claude Opus 5', extraModels: 1, client: 'Claude Code', project: 'ai-usage-cost', started: '8 Sep 09:14', requests: '318', tokens: '12.9M', cost: '$41.88' }}
              onOpen={() => undefined}
            />
          </div>
        </Row>
        <Row title="Detail blocks" hint="What the session drawer is made of.">
          <div className="space-y-4">
            <MetaGrid items={[{ label: 'Client', value: 'Claude Code' }, { label: 'Provider', value: 'anthropic' }, { label: 'Branch', value: 'main' }, { label: 'Subagent thread', value: 'no' }]} />
            <CodeBlock>{'{"match": "claude-opus-6", "input": 5.0, "output": 25.0}'}</CodeBlock>
            <PathList paths={['~/.claude/projects/-home-g-dev-ai-usage-cost/9f3c1a44.jsonl']} />
          </div>
        </Row>
        <Row title="Range and sort controls">
          <div className="flex flex-wrap items-start gap-6">
            <div className="space-y-2">
              <StatLabel>Range</StatLabel>
              <ChipRow options={RANGE_PRESETS} active={range} onSelect={setRange} />
            </div>
            <div className="space-y-2">
              <StatLabel>Dates</StatLabel>
              <DateRange since="2026-08-10" until="2026-09-08" onChange={() => undefined} className="w-56" />
            </div>
            <div className="space-y-2">
              <StatLabel>Sort</StatLabel>
              <SortSelect options={SORT_OPTIONS} value={sort} onChange={setSort} />
            </div>
          </div>
        </Row>
        <Row title="Disclosure and warnings" hint="Readers that ship with the tool but found nothing, and parse warnings from the last scan.">
          <div className="space-y-3">
            <DisclosurePanel title="Available, not detected here" summary="2 more readers ship with the tool and found nothing here: dyad, openai-compat">
              <WarningsList groups={[{ kind: 'other', label: 'Warnings', count: SCAN_WARNINGS.length, summary: `${SCAN_WARNINGS.length} warnings`, warnings: SCAN_WARNINGS }]} />
            </DisclosurePanel>
          </div>
        </Row>
      </Section>

      <Section title="Trace components">
        <Row title="Context occupancy" hint="One bar per model call. Amber is above 85% of the window, the violet tick is a compaction, gaps are calls with no logged capacity.">
          <ContextOccupancy
            points={CONTEXT_SNAPSHOTS}
            formatPercent={formatPercent}
            formatTokens={formatTokens}
            formatClock={formatClock}
          />
        </Row>
        <Row title="Span timeline" hint="Turn structure, coloured by span status and indented by depth.">
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
        </Row>
        <Row title="Insights" hint="Severity is info, warning or critical — never decorative.">
          <InsightList insights={TRACE_INSIGHTS} />
        </Row>
        <Row title="Capabilities" hint="What this source can actually tell you, each answer carrying its own provenance.">
          <CapabilityGrid capabilities={CAPABILITIES} />
        </Row>
      </Section>

      <Panel>
        <PanelNote>
          Every component on this page is the same source the dashboard imports — nothing here is
          a mockup drawn separately.
        </PanelNote>
      </Panel>
    </div>
  )
}
