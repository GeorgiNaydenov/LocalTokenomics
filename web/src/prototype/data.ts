import type { Capabilities, CostState, OutcomeLabel, Provenance, SpanKind, SpanStatus } from '@/api'

export const TODAY = '2026-09-08'

export const DAYS = Array.from({ length: 30 }, (_, index) =>
  new Date(Date.UTC(2026, 7, 10 + index)).toISOString().slice(0, 10),
)

function wave(index: number, base: number, spread: number) {
  const wobble = Math.sin(index * 0.7) * 0.28 + Math.cos(index * 1.9) * 0.16
  const weekend = index % 7 === 5 || index % 7 === 6 ? 0.34 : 1
  return Math.max(0, (base + wobble * spread) * weekend)
}

export interface ModelInfo {
  key: string
  label: string
  provider: string
  client: string
  source: string
  cost: number
  sessions: number
  base: number
  spread: number
  tokens: { uncached_input: number; cache_read: number; cache_write: number; output: number }
  state: CostState
}

export const MODELS: ModelInfo[] = [
  {
    key: 'claude-opus-5',
    label: 'Claude Opus 5',
    provider: 'anthropic',
    client: 'claude-code',
    source: 'claude-code',
    cost: 1489.22,
    sessions: 402,
    base: 49,
    spread: 30,
    tokens: { uncached_input: 4_200_000, cache_read: 38_000_000, cache_write: 6_100_000, output: 1_900_000 },
    state: 'priced',
  },
  {
    key: 'claude-sonnet-5',
    label: 'Claude Sonnet 5',
    provider: 'anthropic',
    client: 'claude-code',
    source: 'claude-code',
    cost: 812.4,
    sessions: 318,
    base: 27,
    spread: 16,
    tokens: { uncached_input: 3_500_000, cache_read: 36_100_000, cache_write: 4_350_000, output: 1_720_000 },
    state: 'priced',
  },
  {
    key: 'gpt-5.2-codex',
    label: 'GPT-5.2 Codex',
    provider: 'openai',
    client: 'codex-cli',
    source: 'codex',
    cost: 604.85,
    sessions: 241,
    base: 20,
    spread: 14,
    tokens: { uncached_input: 2_800_000, cache_read: 24_050_000, cache_write: 2_900_000, output: 1_460_000 },
    state: 'priced',
  },
  {
    key: 'gemini-3-pro',
    label: 'Gemini 3 Pro',
    provider: 'google',
    client: 'antigravity',
    source: 'antigravity',
    cost: 331.07,
    sessions: 147,
    base: 11,
    spread: 8,
    tokens: { uncached_input: 1_900_000, cache_read: 15_200_000, cache_write: 2_180_000, output: 1_120_000 },
    state: 'priced',
  },
  {
    key: 'claude-haiku-4-5',
    label: 'Claude Haiku 4.5',
    provider: 'anthropic',
    client: 'claude-code',
    source: 'claude-code',
    cost: 128.94,
    sessions: 96,
    base: 4.3,
    spread: 3,
    tokens: { uncached_input: 900_000, cache_read: 8_100_000, cache_write: 1_240_000, output: 640_000 },
    state: 'priced',
  },
  {
    key: 'grok-4',
    label: 'Grok 4',
    provider: 'xai',
    client: 'copilot-chat',
    source: 'copilot-chat',
    cost: 0,
    sessions: 24,
    base: 0,
    spread: 0,
    tokens: { uncached_input: 420_000, cache_read: 610_000, cache_write: 98_000, output: 76_000 },
    state: 'unpriced',
  },
  {
    key: 'qwen3-coder',
    label: 'Qwen3 Coder (local)',
    provider: 'ollama',
    client: 'ollama-app',
    source: 'ollama-app',
    cost: 0,
    sessions: 61,
    base: 0,
    spread: 0,
    tokens: { uncached_input: 2_100_000, cache_read: 0, cache_write: 0, output: 1_240_000 },
    state: 'free',
  },
]

export const PRICED_MODELS = MODELS.filter((model) => model.state === 'priced')

export interface SeriesPoint {
  day: string
  model: string
  client: string
  provider: string
  source: string
  cost: number
  tokens: number
  events: number
}

export const SERIES: SeriesPoint[] = DAYS.flatMap((day, index) =>
  MODELS.filter((model) => model.base > 0).map((model, slot) => {
    const cost = Number(wave(index + slot * 3, model.base, model.spread).toFixed(2))
    return {
      day,
      model: model.key,
      client: model.client,
      provider: model.provider,
      source: model.source,
      cost,
      tokens: Math.round(cost * 260_000),
      events: Math.round(cost * 1.9 + 4),
    }
  }),
)

export const CLIENTS = [
  { id: 'claude-code', label: 'Claude Code', count: 21_447 },
  { id: 'codex-cli', label: 'Codex CLI', count: 9_130 },
  { id: 'antigravity', label: 'Antigravity', count: 4_288 },
  { id: 'copilot-chat', label: 'Copilot Chat', count: 3_112 },
  { id: 'ollama-app', label: 'Ollama', count: 1_604 },
  { id: 'jan', label: 'Jan', count: 613 },
]

export const PROJECTS = [
  { key: 'ai-usage-cost', label: 'ai-usage-cost', cost: 1204.66, sessions: 412, events: 14_882 },
  { key: 'atlas-api', label: 'atlas-api', cost: 861.19, sessions: 288, events: 10_114 },
  { key: 'harbor-web', label: 'harbor-web', cost: 655.02, sessions: 231, events: 7_940 },
  { key: 'infra-terraform', label: 'infra-terraform', cost: 402.88, sessions: 147, events: 4_301 },
  { key: 'scratch', label: 'scratch', cost: 219.4, sessions: 96, events: 2_120 },
  { key: 'no-project', label: '(no project)', cost: 88.81, sessions: 61, events: 837 },
]

export interface PrototypeSession {
  id: string
  project: string
  client: string
  provider: string
  models: string[]
  slot: number
  source: string
  started: string
  startedLabel: string
  duration: string
  requests: number
  tokens: { uncached_input: number; cache_read: number; cache_write: number; output: number } | null
  reasoning: number
  cost: number | null
  state: CostState
  provenance: Provenance
  workingDirectory: string | null
  repository: string | null
  branch: string | null
  sidechain: boolean
  machine: string
  rawSource: string[]
  outcome: OutcomeLabel
  traced: boolean
  errorCount: number
}

type SeedSession = Omit<PrototypeSession, 'outcome' | 'traced' | 'errorCount'>

const SEED_SESSIONS: SeedSession[] = [
  {
    id: '9f3c1a44',
    project: 'ai-usage-cost',
    client: 'Claude Code',
    provider: 'anthropic',
    models: ['Claude Opus 5', 'Claude Haiku 4.5'],
    slot: 0,
    source: 'claude-code',
    started: '2026-09-08T09:14:00Z',
    startedLabel: '8 Sep 09:14',
    duration: '1h 42min',
    requests: 318,
    tokens: { uncached_input: 1_159_560, cache_read: 10_049_522, cache_write: 1_159_560, output: 515_361 },
    reasoning: 182_004,
    cost: 41.88,
    state: 'priced',
    provenance: 'measured',
    workingDirectory: '/home/g/dev/ai-usage-cost',
    repository: 'GeorgiNaydenov/ai-usage-cost',
    branch: 'claude/design-system-rebuild',
    sidechain: false,
    machine: 'workstation',
    rawSource: ['~/.claude/projects/-home-g-dev-ai-usage-cost/9f3c1a44.jsonl'],
  },
  {
    id: '7b20de81',
    project: 'atlas-api',
    client: 'Codex CLI',
    provider: 'openai',
    models: ['GPT-5.2 Codex'],
    slot: 2,
    source: 'codex',
    started: '2026-09-08T07:52:00Z',
    startedLabel: '8 Sep 07:52',
    duration: '54min',
    requests: 164,
    tokens: { uncached_input: 576_190, cache_read: 4_993_653, cache_write: 576_190, output: 256_086 },
    reasoning: 94_220,
    cost: 22.4,
    state: 'priced',
    provenance: 'measured',
    workingDirectory: '/home/g/dev/atlas-api',
    repository: 'acme/atlas-api',
    branch: 'main',
    sidechain: false,
    machine: 'workstation',
    rawSource: ['~/.codex/sessions/2026/09/08/rollout-2026-09-08T07-52-00-7b20de81.jsonl'],
  },
  {
    id: 'c41f9a02',
    project: 'harbor-web',
    client: 'Claude Code',
    provider: 'anthropic',
    models: ['Claude Sonnet 5'],
    slot: 1,
    source: 'claude-code',
    started: '2026-09-07T21:03:00Z',
    startedLabel: '7 Sep 21:03',
    duration: '2h 18min',
    requests: 402,
    tokens: { uncached_input: 1_620_310, cache_read: 14_042_684, cache_write: 1_620_310, output: 720_137 },
    reasoning: 0,
    cost: 31.07,
    state: 'priced',
    provenance: 'measured',
    workingDirectory: '/home/g/dev/harbor-web',
    repository: 'acme/harbor-web',
    branch: 'feat/checkout',
    sidechain: false,
    machine: 'workstation',
    rawSource: ['~/.claude/projects/-home-g-dev-harbor-web/c41f9a02.jsonl'],
  },
  {
    id: 'a1b0ff37',
    project: 'ai-usage-cost',
    client: 'Claude Code',
    provider: 'anthropic',
    models: ['Claude Opus 5'],
    slot: 0,
    source: 'claude-code',
    started: '2026-09-07T18:20:00Z',
    startedLabel: '7 Sep 18:20',
    duration: '36min',
    requests: 118,
    tokens: { uncached_input: 402_110, cache_read: 3_480_002, cache_write: 402_110, output: 179_004 },
    reasoning: 61_220,
    cost: 14.62,
    state: 'priced',
    provenance: 'measured',
    workingDirectory: '/home/g/dev/ai-usage-cost',
    repository: 'GeorgiNaydenov/ai-usage-cost',
    branch: 'main',
    sidechain: true,
    machine: 'workstation',
    rawSource: ['~/.claude/projects/-home-g-dev-ai-usage-cost/a1b0ff37.jsonl'],
  },
  {
    id: 'd8e7b310',
    project: 'infra-terraform',
    client: 'Antigravity',
    provider: 'google',
    models: ['Gemini 3 Pro'],
    slot: 3,
    source: 'antigravity',
    started: '2026-09-07T16:41:00Z',
    startedLabel: '7 Sep 16:41',
    duration: '38min',
    requests: 91,
    tokens: null,
    reasoning: 0,
    cost: null,
    state: 'unavailable',
    provenance: 'unavailable',
    workingDirectory: '/home/g/infra',
    repository: null,
    branch: null,
    sidechain: false,
    machine: 'workstation',
    rawSource: ['~/.gemini/antigravity/brain/2f1a/.system_generated/logs/transcript_full.jsonl'],
  },
  {
    id: '2a5c6f77',
    project: 'scratch',
    client: 'Ollama',
    provider: 'ollama',
    models: ['Qwen3 Coder (local)'],
    slot: 6,
    source: 'ollama-app',
    started: '2026-09-07T14:22:00Z',
    startedLabel: '7 Sep 14:22',
    duration: '1h 09min',
    requests: 220,
    tokens: { uncached_input: 2_100_000, cache_read: 0, cache_write: 0, output: 1_240_000 },
    reasoning: 0,
    cost: 0,
    state: 'free',
    provenance: 'derived',
    workingDirectory: null,
    repository: null,
    branch: null,
    sidechain: false,
    machine: 'laptop',
    rawSource: ['%LOCALAPPDATA%\\Ollama\\db.sqlite'],
  },
  {
    id: 'e0193bcd',
    project: 'atlas-api',
    client: 'Copilot Chat',
    provider: 'xai',
    models: ['Grok 4'],
    slot: 5,
    source: 'copilot-chat',
    started: '2026-09-06T11:47:00Z',
    startedLabel: '6 Sep 11:47',
    duration: '26min',
    requests: 58,
    tokens: { uncached_input: 420_000, cache_read: 610_000, cache_write: 98_000, output: 76_000 },
    reasoning: 0,
    cost: null,
    state: 'unpriced',
    provenance: 'estimated',
    workingDirectory: '/home/g/dev/atlas-api',
    repository: 'acme/atlas-api',
    branch: 'main',
    sidechain: false,
    machine: 'workstation',
    rawSource: ['<vscode-data>/User/globalStorage/github.copilot-chat/session-store.db'],
  },
  {
    id: 'ab77c209',
    project: 'ai-usage-cost',
    client: 'Claude Code',
    provider: 'anthropic',
    models: ['Claude Haiku 4.5'],
    slot: 4,
    source: 'claude-code',
    started: '2026-09-06T09:12:00Z',
    startedLabel: '6 Sep 09:12',
    duration: '12min',
    requests: 44,
    tokens: { uncached_input: 81_209, cache_read: 703_818, cache_write: 81_209, output: 36_095 },
    reasoning: 0,
    cost: 1.14,
    state: 'priced',
    provenance: 'measured',
    workingDirectory: '/home/g/dev/ai-usage-cost',
    repository: 'GeorgiNaydenov/ai-usage-cost',
    branch: 'main',
    sidechain: false,
    machine: 'workstation',
    rawSource: ['~/.claude/projects/-home-g-dev-ai-usage-cost/ab77c209.jsonl'],
  },
  {
    id: '5cd8e441',
    project: 'harbor-web',
    client: 'Jan',
    provider: 'jan',
    models: ['Qwen3 Coder (local)'],
    slot: 6,
    source: 'jan',
    started: '2026-09-05T19:30:00Z',
    startedLabel: '5 Sep 19:30',
    duration: '47min',
    requests: 133,
    tokens: null,
    reasoning: 0,
    cost: null,
    state: 'unavailable',
    provenance: 'unavailable',
    workingDirectory: null,
    repository: null,
    branch: null,
    sidechain: false,
    machine: 'laptop',
    rawSource: ['~/jan/threads/5cd8e441/messages.jsonl'],
  },
]

export interface SourceRecord {
  id: string
  label: string
  path: string
  rootHint: string
  clients: string[]
  hasTokens: boolean
  detected: boolean
  files: number
  sessions: number
  requests: number
  cost: number
  lastEvent: string | null
  slot: number
}

export const SOURCES: SourceRecord[] = [
  {
    id: 'claude-code',
    label: 'Claude Code',
    path: '~/.claude/projects/*/*.jsonl',
    rootHint: '~/.claude',
    clients: ['claude-code'],
    hasTokens: true,
    detected: true,
    files: 412,
    sessions: 816,
    requests: 21_447,
    cost: 2_430.56,
    lastEvent: '2026-09-08',
    slot: 0,
  },
  {
    id: 'codex',
    label: 'Codex',
    path: '~/.codex/sessions/**/rollout-*.jsonl',
    rootHint: '~/.codex',
    clients: ['codex-cli', 'codex-desktop'],
    hasTokens: true,
    detected: true,
    files: 208,
    sessions: 241,
    requests: 9_130,
    cost: 604.85,
    lastEvent: '2026-09-08',
    slot: 1,
  },
  {
    id: 'antigravity',
    label: 'Google Antigravity',
    path: '~/.gemini/antigravity/brain/*/.system_generated/logs/transcript*.jsonl',
    rootHint: '~/.gemini/antigravity',
    clients: ['antigravity'],
    hasTokens: false,
    detected: true,
    files: 94,
    sessions: 147,
    requests: 4_288,
    cost: 0,
    lastEvent: '2026-09-07',
    slot: 2,
  },
  {
    id: 'copilot-chat',
    label: 'GitHub Copilot Chat',
    path: '<vscode-data>/User/globalStorage/github.copilot-chat/session-store.db',
    rootHint: '<vscode-data>',
    clients: ['copilot-chat'],
    hasTokens: false,
    detected: true,
    files: 1,
    sessions: 24,
    requests: 3_112,
    cost: 0,
    lastEvent: '2026-09-06',
    slot: 3,
  },
  {
    id: 'ollama-app',
    label: 'Ollama app',
    path: '%LOCALAPPDATA%\\Ollama\\db.sqlite',
    rootHint: '%LOCALAPPDATA%\\Ollama',
    clients: ['ollama-app'],
    hasTokens: false,
    detected: true,
    files: 1,
    sessions: 61,
    requests: 1_604,
    cost: 0,
    lastEvent: '2026-09-07',
    slot: 4,
  },
  {
    id: 'jan',
    label: 'Jan',
    path: '~/jan/threads',
    rootHint: '~/jan',
    clients: ['jan'],
    hasTokens: false,
    detected: true,
    files: 71,
    sessions: 32,
    requests: 613,
    cost: 0,
    lastEvent: '2026-09-05',
    slot: 5,
  },
  {
    id: 'dyad',
    label: 'Dyad',
    path: '<app-data>/dyad/sqlite.db',
    rootHint: '<app-data>/dyad',
    clients: ['dyad'],
    hasTokens: false,
    detected: false,
    files: 0,
    sessions: 0,
    requests: 0,
    cost: 0,
    lastEvent: null,
    slot: 6,
  },
  {
    id: 'openai-compat',
    label: 'OpenAI-compatible',
    path: 'none by default, pass --root openai-compat=PATH',
    rootHint: 'no default root',
    clients: ['openai-compat'],
    hasTokens: true,
    detected: false,
    files: 0,
    sessions: 0,
    requests: 0,
    cost: 0,
    lastEvent: null,
    slot: 7,
  },
]

export function sourceTrend(sourceId: string, useCost: boolean): number[] {
  if (useCost) {
    return DAYS.map((day) =>
      SERIES.filter((point) => point.day === day && point.source === sourceId).reduce(
        (sum, point) => sum + point.cost,
        0,
      ),
    )
  }
  const source = SOURCES.find((entry) => entry.id === sourceId)
  const average = source ? source.requests / DAYS.length : 0
  return DAYS.map((_, index) => Math.round(wave(index + (source?.slot ?? 0) * 4, average, average * 0.6)))
}

export interface RateRow {
  match: string
  provider: string
  display: string
  input: number
  output: number
  inherited: boolean
  spend: number
}

export const RATES: RateRow[] = [
  { match: 'claude-opus-5', provider: 'anthropic', display: 'Claude Opus 5', input: 5, output: 25, inherited: false, spend: 1489.22 },
  { match: 'claude-sonnet-5', provider: 'anthropic', display: 'Claude Sonnet 5', input: 3, output: 15, inherited: false, spend: 812.4 },
  { match: 'gpt-5.2-codex', provider: 'openai', display: 'GPT-5.2 Codex', input: 1.75, output: 14, inherited: false, spend: 604.85 },
  { match: 'gemini-3-pro', provider: 'google', display: 'Gemini 3 Pro', input: 1.25, output: 10, inherited: false, spend: 331.07 },
  { match: 'claude-haiku-4-5', provider: 'anthropic', display: 'Claude Haiku 4.5', input: 0.8, output: 4, inherited: false, spend: 128.94 },
  { match: 'qwen3-coder', provider: 'ollama', display: 'Qwen3 Coder', input: 0, output: 0, inherited: false, spend: 0 },
  { match: 'claude-opus-4-1', provider: 'anthropic', display: 'Claude Opus 4.1', input: 15, output: 75, inherited: true, spend: 0 },
  { match: 'gpt-5.1', provider: 'openai', display: 'GPT-5.1', input: 1.25, output: 10, inherited: false, spend: 0 },
  { match: 'gemini-2-5-flash', provider: 'google', display: 'Gemini 2.5 Flash', input: 0.3, output: 2.5, inherited: false, spend: 0 },
  { match: 'deepseek-v3', provider: 'deepseek', display: 'DeepSeek V3', input: 0.27, output: 1.1, inherited: false, spend: 0 },
  { match: 'kimi-k2', provider: 'moonshot', display: 'Kimi K2', input: 0.6, output: 2.5, inherited: false, spend: 0 },
  { match: 'mistral-large', provider: 'mistral', display: 'Mistral Large', input: 2, output: 6, inherited: false, spend: 0 },
]

export interface ProviderRules {
  cache_read: number
  cache_write_5m: number
  cache_write_1h: number
  batch: number
}

export const PROVIDER_RULES: Record<string, ProviderRules> = {
  anthropic: { cache_read: 0.1, cache_write_5m: 1.25, cache_write_1h: 2.0, batch: 0.5 },
  openai: { cache_read: 0.25, cache_write_5m: 1.0, cache_write_1h: 1.0, batch: 0.5 },
  google: { cache_read: 0.25, cache_write_5m: 1.0, cache_write_1h: 1.0, batch: 0.5 },
}

export const UNKNOWN_MODELS = [{ model: 'grok-4', tokens: 1_204_000, events: 58 }]

export const SCAN_WARNINGS = [
  '~/.codex/sessions/2026/08/22/rollout-2026-08-22T11-04-19-3f2a.jsonl: 2 lines could not be parsed as JSON',
  '~/jan/threads/91ac/messages.jsonl: no timestamp on 4 messages, those requests were skipped',
]

export const TOTALS = {
  cost: 3_431.96,
  noCacheEquivalent: 16_316.27,
  cacheSavings: 12_884.31,
  requests: 40_194,
  sessions: 1_235,
  files: 787,
  tokens: {
    total: 411_882_004,
    uncached_input: 34_120_000,
    cache_read: 321_902_004,
    cache_write: 38_920_000,
    output: 16_940_000,
  },
  ratesAsOf: '2026-09-07',
}

export const FACET_COUNTS = {
  states: { priced: 34_118, free: 1_604, unpriced: 1_072, unavailable: 3_400 } as Record<string, number>,
  clients: Object.fromEntries(CLIENTS.map((client) => [client.id, client.count])),
  models: Object.fromEntries(MODELS.map((model) => [model.key, model.sessions * 26])),
  projects: Object.fromEntries(PROJECTS.map((project) => [project.key, project.events])),
}

export const SAVED_VIEWS = [
  { value: 'all', label: 'All usage' },
  { value: 'week', label: 'Last 7 days' },
  { value: 'gaps', label: 'Missing token data' },
  { value: 'main', label: 'Main thread only' },
  { value: 'top-model', label: 'Top model' },
]

export const RANGE_PRESETS = [
  { value: '1', label: 'Today' },
  { value: '14', label: '14 d' },
  { value: '30', label: '30 d' },
  { value: '60', label: '60 d' },
  { value: '90', label: '90 d' },
  { value: '180', label: '180 d' },
  { value: 'all', label: 'All' },
]

export const SORT_OPTIONS = [
  { value: 'cost:desc', label: 'Cost, high to low' },
  { value: 'cost:asc', label: 'Cost, low to high' },
  { value: 'tokens:desc', label: 'Tokens, high to low' },
  { value: 'start:desc', label: 'Newest first' },
  { value: 'start:asc', label: 'Oldest first' },
  { value: 'requests:desc', label: 'Most requests' },
  { value: 'state:asc', label: 'Cost state' },
  { value: 'project:asc', label: 'Project A to Z' },
]

export const PROJECT_PEAK = Math.max(...PROJECTS.map((project) => project.cost), 0.01)

function perDay(pick: (point: SeriesPoint) => number): number[] {
  return DAYS.map((day) =>
    SERIES.filter((point) => point.day === day).reduce((sum, point) => sum + pick(point), 0),
  )
}

const costPerDay = perDay((point) => point.cost)

export const PROTOTYPE_SLICE = {
  costPerDay,
  cacheReadPerDay: perDay((point) => point.tokens * 0.78),
  requestsPerDay: perDay((point) => point.events),
  sessionsPerDay: perDay((point) => point.events / 32),
  cacheSavedPerDay: costPerDay.map((value) => value * 3.75),
  clientLabel: (id: string) => CLIENTS.find((client) => client.id === id)?.label ?? id,
  modelLabel: (id: string) => MODELS.find((model) => model.key === id)?.label ?? id,
  sourceLabel: (id: string) => SOURCES.find((source) => source.id === id)?.label ?? id,
}

const OUTCOMES: OutcomeLabel[] = ['successful', 'partial', 'failed', 'abandoned', 'unrated']

function outcomeFor(index: number, state: CostState): OutcomeLabel {
  if (state === 'unavailable') return 'unrated'
  return OUTCOMES[index % OUTCOMES.length]
}

export const SESSIONS: PrototypeSession[] = (() => {
  const seeded: PrototypeSession[] = SEED_SESSIONS.map((session, index) => ({
    ...session,
    outcome: outcomeFor(index, session.state),
    traced: session.state !== 'unavailable' && index % 3 !== 2,
    errorCount: index % 4 === 1 ? index % 3 : 0,
  }))

  const generated: PrototypeSession[] = []
  for (let index = 0; generated.length + seeded.length < 184; index++) {
    const base = seeded[index % seeded.length]
    const day = DAYS[(DAYS.length - 1 - (index % DAYS.length)) % DAYS.length]
    const hour = 6 + (index % 14)
    const minute = (index * 7) % 60
    const scale = 0.22 + ((index * 37) % 100) / 130
    const stamp = `${day}T${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}:00Z`
    const requests = Math.max(3, Math.round(base.requests * scale))
    generated.push({
      ...base,
      id: (0x10000000 + index * 2654435761).toString(16).slice(-8),
      started: stamp,
      startedLabel: `${Number(day.slice(8))} ${
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][
          Number(day.slice(5, 7)) - 1
        ]
      } ${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`,
      requests,
      tokens: base.tokens
        ? {
            uncached_input: Math.round(base.tokens.uncached_input * scale),
            cache_read: Math.round(base.tokens.cache_read * scale),
            cache_write: Math.round(base.tokens.cache_write * scale),
            output: Math.round(base.tokens.output * scale),
          }
        : null,
      reasoning: Math.round(base.reasoning * scale),
      cost: base.cost === null ? null : Number((base.cost * scale).toFixed(2)),
      outcome: outcomeFor(index + 2, base.state),
      traced: base.state !== 'unavailable' && index % 4 !== 3,
      errorCount: index % 6 === 0 ? (index % 3) + 1 : 0,
    })
  }

  return [...seeded, ...generated]
})()

export const SESSION_LIMIT = 120

export const OUTCOME_COUNTS: Record<OutcomeLabel, number> = SESSIONS.reduce(
  (counts, session) => {
    counts[session.outcome] += 1
    return counts
  },
  { successful: 0, partial: 0, failed: 0, abandoned: 0, unrated: 0 } as Record<OutcomeLabel, number>,
)

export const TRACED_COUNT = SESSIONS.filter((session) => session.traced).length
export const ERROR_COUNT = SESSIONS.filter((session) => session.errorCount > 0).length

export const CAPABILITIES: Capabilities = {
  trace: 'measured',
  tokens: 'measured',
  cost: 'derived',
  context: 'estimated',
  latency: 'measured',
}

export interface OccupancySnapshot {
  spanId: string
  startedAt: string
  occupancy: number | null
  inputTotal: number | null
  capacity: number | null
  compactedBefore: boolean
}

export const CONTEXT_SNAPSHOTS: OccupancySnapshot[] = Array.from({ length: 46 }, (_, index) => {
  const compactedBefore = index === 19 || index === 34
  const cycle = index < 19 ? index / 19 : index < 34 ? (index - 19) / 15 : (index - 34) / 12
  const occupancy = index === 7 || index === 8 ? null : Math.min(0.97, 0.16 + cycle * 0.78)
  const capacity = 200_000
  return {
    spanId: `span-${index}`,
    startedAt: `2026-09-08T${String(9 + Math.floor(index / 8)).padStart(2, '0')}:${String(
      (index * 6) % 60,
    ).padStart(2, '0')}:00Z`,
    occupancy,
    inputTotal: occupancy === null ? null : Math.round(occupancy * capacity),
    capacity,
    compactedBefore,
  }
})

export interface TraceSpanRecord {
  spanId: string
  kind: SpanKind
  name: string
  status: SpanStatus
  depth: number
  durationMs: number | null
  tokens: number | null
}

export const TRACE_SPANS: TraceSpanRecord[] = [
  { spanId: 's1', kind: 'turn', name: 'Turn 14 — rebuild the design system', status: 'ok', depth: 0, durationMs: 184_000, tokens: 412_004 },
  { spanId: 's2', kind: 'user', name: 'User message', status: 'ok', depth: 1, durationMs: null, tokens: 1_204 },
  { spanId: 's3', kind: 'model_call', name: 'claude-opus-5', status: 'ok', depth: 1, durationMs: 21_400, tokens: 188_320 },
  { spanId: 's4', kind: 'reasoning', name: 'Reasoning', status: 'ok', depth: 2, durationMs: 8_200, tokens: 42_110 },
  { spanId: 's5', kind: 'tool_call', name: 'Read web/src/Overview.tsx', status: 'ok', depth: 2, durationMs: 140, tokens: null },
  { spanId: 's6', kind: 'tool_result', name: '633 lines', status: 'ok', depth: 3, durationMs: null, tokens: 18_902 },
  { spanId: 's7', kind: 'tool_call', name: 'Edit web/src/components/status.tsx', status: 'interrupted', depth: 2, durationMs: 90, tokens: null },
  { spanId: 's8', kind: 'error', name: 'File changed on disk, retrying', status: 'error', depth: 2, durationMs: null, tokens: null },
  { spanId: 's9', kind: 'subagent', name: 'Explore — find chart callers', status: 'ok', depth: 1, durationMs: 46_000, tokens: 94_220 },
  { spanId: 's10', kind: 'compaction', name: 'Context compacted', status: 'ok', depth: 1, durationMs: 3_100, tokens: null },
  { spanId: 's11', kind: 'assistant', name: 'Assistant reply', status: 'ok', depth: 1, durationMs: null, tokens: 8_440 },
]

export const TRACE_INSIGHTS = [
  {
    kind: 'context_pressure',
    severity: 'warning' as const,
    message: 'Context reached 97% before the second compaction. Two model calls ran with no room for tool results.',
  },
  {
    kind: 'retry',
    severity: 'info' as const,
    message: 'One tool call was interrupted and retried once. The retry succeeded.',
  },
  {
    kind: 'cache',
    severity: 'info' as const,
    message: '78% of input came from cache, which is where most of the saving on this session comes from.',
  },
]
