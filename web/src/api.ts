export interface TokenUsage {
  uncached_input: number
  cache_read: number
  cache_write_5m: number
  cache_write_1h: number
  output: number
  reasoning_output: number
  cache_write: number
  input_total: number
  total: number
}

export interface CostBreakdown {
  uncached_input: number
  cache_read: number
  cache_write: number
  output: number
  no_cache_equivalent: number
  total: number
  cache_savings: number
}

export interface Bucket {
  key: string
  label: string
  tokens: TokenUsage
  cost: CostBreakdown
  events: number
  sessions: number
}

export interface Totals {
  tokens: TokenUsage
  cost: CostBreakdown
  events: number
  sessions: number
  first_event: string | null
  last_event: string | null
}

export interface SeriesPoint {
  day: string
  client: string
  provider: string
  model: string
  source: string
  cost: number
  tokens: number
  events: number
}

export type CostState = 'priced' | 'free' | 'unpriced' | 'unavailable'

export type Provenance = 'measured' | 'derived' | 'estimated' | 'inferred' | 'unavailable'

export type RawScalar = string | number | boolean | null

export type SpanKind =
  | 'turn'
  | 'user'
  | 'assistant'
  | 'reasoning'
  | 'model_call'
  | 'tool_call'
  | 'tool_result'
  | 'retrieval'
  | 'compaction'
  | 'error'
  | 'subagent'

export type SpanStatus = 'ok' | 'error' | 'interrupted' | 'aborted' | 'running' | 'unknown'

export type OutcomeLabel = 'successful' | 'partial' | 'failed' | 'abandoned' | 'unrated'

export interface Span {
  span_id: string
  parent_id: string | null
  record_parent: string | null
  source: string
  session_id: string
  turn_id: string | null
  agent_id: string | null
  is_sidechain: boolean
  seq: number
  kind: SpanKind
  name: string | null
  model: string | null
  status: SpanStatus
  started_at: string
  ended_at: string | null
  duration_ms: number | null
  duration_provenance: Provenance
  ttft_ms: number | null
  tokens: TokenUsage | null
  tokens_provenance: Provenance
  context_capacity: number | null
  capacity_provenance: Provenance
  retry_attempt: number | null
  error: string | null
  source_file: string
  record_offset: number
  record_length: number
  content_path: string | null
  detail: Record<string, RawScalar>
}

export interface Capabilities {
  trace: Provenance
  tokens: Provenance
  cost: Provenance
  context: Provenance
  latency: Provenance
}

export interface ContextSnapshot {
  span_id: string
  model: string | null
  started_at: string
  input_total: number | null
  tokens_provenance: Provenance
  capacity: number | null
  capacity_provenance: Provenance
  occupancy: number | null
  occupancy_provenance: Provenance
  delta_input: number | null
  added_span_ids: string[]
  compacted_before: boolean
}

export interface OutcomeSignals {
  aborted_turns: number
  interrupted_tools: number
  errors: number
  last_turn_status: SpanStatus
}

export interface OutcomeUpdate {
  outcome: OutcomeLabel
  notes: string
  tags: string[]
}

export interface Outcome extends OutcomeUpdate {
  source: string
  session_id: string
  updated_at: string | null
  signals: OutcomeSignals
}

export interface EconRow {
  key: string
  label: string
  model_calls: number
  tool_calls: number
  tokens: TokenUsage
  cost: CostBreakdown | null
  cost_state: CostState
  duration_ms: number | null
  duration_provenance: Provenance
  errors: number
  retries: number | null
  amplification: number | null
  cache_hit_ratio: number | null
  tokens_per_second: number | null
}

export interface Economics {
  totals: EconRow
  by_turn: EconRow[]
  by_model: EconRow[]
  by_tool: EconRow[]
}

export interface Insight {
  kind: string
  severity: 'info' | 'warning' | 'critical'
  span_id: string
  message: string
}

export interface Trace {
  source: string
  session_id: string
  capabilities: Capabilities
  spans: Span[]
  outcome: Outcome | null
  insights: Insight[]
}

export interface SpanContent {
  span_id: string
  content: string
  truncated: boolean
  redactions: number
}

export interface DeletedSession {
  deleted_spans: number
}

export interface SessionRow {
  session_id: string
  source: string
  client: string
  provider: string
  models: string[]
  start_time: string
  end_time: string
  request_count: number
  tokens: TokenUsage | null
  cost: CostBreakdown | null
  cost_state: CostState
  cost_states: CostState[]
  is_sidechain: boolean
  currency: string
  project: string | null
  working_directory: string | null
  repository: string | null
  branch: string | null
  machine: string
  raw_source: string[]
  outcome: OutcomeLabel
  traced: boolean
  error_count: number
}

export interface UnknownModel {
  model: string
  tokens: number
  events: number
}

export interface Facets {
  states: Record<string, number>
  clients: Record<string, number>
  models: Record<string, number>
  projects: Record<string, number>
  outcomes: Record<string, number>
}

export interface Report {
  generated_at: string
  rates_as_of: string
  currency: string
  files_scanned: number
  totals: Totals
  by_client: Bucket[]
  by_provider: Bucket[]
  by_model: Bucket[]
  by_project: Bucket[]
  by_day: Bucket[]
  series: SeriesPoint[]
  sessions: SessionRow[]
  unknown_models: UnknownModel[]
  warnings: string[]
  scan_warnings: string[]
  facets: Facets
}

export interface ClientInfo {
  id: string
  label: string
}

export type TokenDataKind = 'full' | 'session'

export interface SourceInfo {
  id: string
  label: string
  clients: string[]
  token_data: TokenDataKind
  path: string
  root_hint: string
  detected: boolean
  files: number
  capabilities: Capabilities
}

export interface Meta {
  clients: ClientInfo[]
  providers: string[]
  models: string[]
  projects: string[]
  first_day: string | null
  last_day: string | null
  rates_as_of: string
  currency: string
  files_scanned: number
  events: number
  warnings: string[]
  sources: SourceInfo[]
}

export type View = 'overview' | 'sessions' | 'sources' | 'pricing'

export type FacetGroup = 'states' | 'clients' | 'models' | 'projects'

export interface Query {
  since: string | null
  until: string | null
  search: string
  states: CostState[]
  clients: string[]
  models: string[]
  projects: string[]
  includeSidechains: boolean
  outcomes: OutcomeLabel[]
  traced: boolean | null
  hasErrors: boolean | null
}

export interface RateVariant {
  input: number
  output: number
}

export interface ProviderRules {
  cache_read: number
  cache_write_5m: number
  cache_write_1h: number
  batch: number
  free: boolean
}

export interface ModelRate {
  match: string
  provider: string
  display: string
  input: number
  output: number
  variants: Record<string, RateVariant>
  cache_rules: ProviderRules | null
  inherited: boolean
}

export interface RatePrefix {
  prefix: string
  provider: string | null
}

export interface RateTable {
  as_of: string
  currency: string
  units: string
  notes: string[]
  prefixes: RatePrefix[]
  providers: Record<string, ProviderRules>
  models: ModelRate[]
}

export class ApiError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'ApiError'
  }
}

async function getJson<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response
  try {
    response = await fetch(path, init)
  } catch {
    throw new ApiError('Could not reach the ai-usage-cost server. Is it still running?')
  }
  if (!response.ok) {
    throw new ApiError(`${path} responded ${response.status} ${response.statusText}`)
  }
  return (await response.json()) as T
}

export function fetchMeta(signal?: AbortSignal): Promise<Meta> {
  return getJson<Meta>('api/meta', { signal })
}

export function refresh(): Promise<Meta> {
  return getJson<Meta>('api/refresh', { method: 'POST' })
}

export function fetchRates(signal?: AbortSignal): Promise<RateTable> {
  return getJson<RateTable>('api/rates', { signal })
}

export function reportUrl(query: Query): string {
  const params = new URLSearchParams()
  if (query.since) params.set('since', query.since)
  if (query.until) params.set('until', query.until)
  const search = query.search.trim()
  if (search) params.set('search', search)
  const appendAll = (name: string, values: string[]) => {
    for (const value of values) params.append(name, value)
  }
  appendAll('states', query.states)
  appendAll('clients', query.clients)
  appendAll('models', query.models)
  appendAll('projects', query.projects)
  appendAll('outcomes', query.outcomes)
  if (!query.includeSidechains) params.set('include_sidechains', 'false')
  if (query.traced !== null) params.set('traced', String(query.traced))
  if (query.hasErrors !== null) params.set('has_errors', String(query.hasErrors))
  const queryString = params.toString()
  return queryString ? `api/report?${queryString}` : 'api/report'
}

export function fetchReport(query: Query, signal?: AbortSignal): Promise<Report> {
  return getJson<Report>(reportUrl(query), { signal })
}

function sessionPath(source: string, sessionId: string): string {
  return `api/sessions/${encodeURIComponent(source)}/${encodeURIComponent(sessionId)}`
}

export function fetchTrace(source: string, sessionId: string, signal?: AbortSignal): Promise<Trace> {
  return getJson<Trace>(`${sessionPath(source, sessionId)}/trace`, { signal })
}

export function fetchEconomics(
  source: string,
  sessionId: string,
  signal?: AbortSignal,
): Promise<Economics> {
  return getJson<Economics>(`${sessionPath(source, sessionId)}/economics`, { signal })
}

export function fetchContext(
  source: string,
  sessionId: string,
  signal?: AbortSignal,
): Promise<ContextSnapshot[]> {
  return getJson<ContextSnapshot[]>(`${sessionPath(source, sessionId)}/context`, { signal })
}

export function fetchOutcome(
  source: string,
  sessionId: string,
  signal?: AbortSignal,
): Promise<Outcome> {
  return getJson<Outcome>(`${sessionPath(source, sessionId)}/outcome`, { signal })
}

export function putOutcome(
  source: string,
  sessionId: string,
  update: OutcomeUpdate,
): Promise<Outcome> {
  return getJson<Outcome>(`${sessionPath(source, sessionId)}/outcome`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(update),
  })
}

export function fetchSpanContent(
  source: string,
  sessionId: string,
  spanId: string,
  signal?: AbortSignal,
): Promise<SpanContent> {
  const path = `${sessionPath(source, sessionId)}/spans/${encodeURIComponent(spanId)}/content`
  return getJson<SpanContent>(path, { signal })
}

export function deleteSession(source: string, sessionId: string): Promise<DeletedSession> {
  return getJson<DeletedSession>(sessionPath(source, sessionId), { method: 'DELETE' })
}
