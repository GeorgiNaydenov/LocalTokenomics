/** Types mirror the FastAPI response models in src/ai_usage_cost/. */

export interface TokenUsage {
  uncached_input: number
  cache_read: number
  cache_write_5m: number
  cache_write_1h: number
  output: number
  reasoning_output: number
  thinking_output: number
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
  tool: string
  model: string
  cost: number
  tokens: number
}

export interface SessionRow {
  session_id: string
  tool: string
  project: string | null
  models: string[]
  started: string
  ended: string
  events: number
  tokens: number
  cost: number
}

export interface UnknownModel {
  model: string
  tokens: number
  events: number
}

export interface Report {
  generated_at: string
  rates_as_of: string
  files_scanned: number
  totals: Totals
  by_tool: Bucket[]
  by_model: Bucket[]
  by_project: Bucket[]
  by_day: Bucket[]
  series: SeriesPoint[]
  sessions: SessionRow[]
  unknown_models: UnknownModel[]
  warnings: string[]
}

export interface ToolInfo {
  id: string
  label: string
}

export interface Meta {
  tools: ToolInfo[]
  models: string[]
  projects: string[]
  first_day: string | null
  last_day: string | null
  rates_as_of: string
  files_scanned: number
  events: number
  warnings: string[]
}

export interface ReportQuery {
  since: string | null
  until: string | null
  tools: string[]
  models: string[]
  projects: string[]
  includeSidechains: boolean
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
    throw new ApiError(
      'Could not reach the ai-usage-cost server. Is it still running on port 8420?',
    )
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

/** Repeatable params are only sent when they actually narrow the result. */
export function reportUrl(query: ReportQuery, meta: Meta | null): string {
  const params = new URLSearchParams()
  if (query.since) params.set('since', query.since)
  if (query.until) params.set('until', query.until)
  const append = (name: string, chosen: string[], all: string[]) => {
    if (chosen.length === 0 || chosen.length === all.length) return
    for (const value of chosen) params.append(name, value)
  }
  append('tools', query.tools, meta?.tools.map((tool) => tool.id) ?? [])
  append('models', query.models, meta?.models ?? [])
  append('projects', query.projects, meta?.projects ?? [])
  if (!query.includeSidechains) params.set('include_sidechains', 'false')
  const search = params.toString()
  return search ? `api/report?${search}` : 'api/report'
}

export function fetchReport(
  query: ReportQuery,
  meta: Meta | null,
  signal?: AbortSignal,
): Promise<Report> {
  return getJson<Report>(reportUrl(query, meta), { signal })
}
