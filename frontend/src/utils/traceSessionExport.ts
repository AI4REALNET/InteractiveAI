import type { Trace } from '@/types/services'

type ExportFormat = 'json' | 'csv'
type SessionStep = Trace['step'] | 'FEEDBACK'

type StoredTrace = {
  date: string
  use_case: Trace['use_case']
  step: SessionStep
  data: unknown
}

type TraceSession = {
  sessionId: string
  startedAt: string
  userLogin?: string
  traces: StoredTrace[]
}

type ExportOptions = {
  force?: boolean
  userLogin?: string
}

const STORAGE_KEY = 'interactiveai.trace-session.v1'

function generateSessionId() {
  if (window.isSecureContext && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID()
  }
  return '10000000-1000-4000-8000-100000000000'.replace(/[018]/g, (char) =>
    (+char ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (+char / 4)))).toString(16)
  )
}

function createSession(userLogin?: string): TraceSession {
  return {
    sessionId: generateSessionId(),
    startedAt: new Date().toISOString(),
    userLogin,
    traces: []
  }
}

function loadSession(): TraceSession | undefined {
  const raw = localStorage.getItem(STORAGE_KEY)
  if (!raw) return undefined
  try {
    return JSON.parse(raw) as TraceSession
  } catch {
    localStorage.removeItem(STORAGE_KEY)
    return undefined
  }
}

function saveSession(session: TraceSession) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(session))
}

function eventKey(data: unknown): string | undefined {
  if (!data || typeof data !== 'object') return undefined
  const candidate = data as { card_id?: unknown; process_instance_id?: unknown }
  if (typeof candidate.card_id === 'string') return `card:${candidate.card_id}`
  if (typeof candidate.process_instance_id === 'string') return `process:${candidate.process_instance_id}`
  return undefined
}

/**
 * Build a structured view: nest ASKFORHELP/FEEDBACK/AWARD under the EVENT they belong to.
 *
 * Algorithm:
 *  1. Walk traces in chronological order.
 *  2. Every EVENT becomes a top-level structured entry (with an `interactions` array).
 *  3. An ASKFORHELP opens a "current interaction group" linked to an EVENT via card_id.
 *  4. Subsequent FEEDBACK / AWARD traces are appended to that group until a new ASKFORHELP or EVENT appears.
 *  5. Traces that cannot be linked to any EVENT remain at the top level as-is.
 */
type StructuredEvent = StoredTrace & {
  interactions: StoredTrace[]
  /** Time in ms between ASKFORHELP and AWARD. null when the user didn't choose a solution. */
  decision_time_ms: number | null
}

type StructuredTrace = StoredTrace | StructuredEvent

type SessionKpis = {
  /** Total session duration in ms (endedAt − startedAt) */
  total_session_time_ms: number
  /** Average decision time across ALL events (sum of decision times / total events). null if no events. */
  avg_decision_time_ms: number | null
}

function isStructuredEvent(t: StructuredTrace): t is StructuredEvent {
  return 'interactions' in t
}

function computeDecisionTime(interactions: StoredTrace[]): number | null {
  let askDate: string | undefined
  let awardDate: string | undefined
  for (let i = 0; i < interactions.length; i++) {
    if (interactions[i].step === 'ASKFORHELP' && !askDate) askDate = interactions[i].date
    if (interactions[i].step === 'AWARD' && !awardDate) awardDate = interactions[i].date
  }
  if (!askDate || !awardDate) return null
  return new Date(awardDate).getTime() - new Date(askDate).getTime()
}

function buildStructuredTraces(flat: StoredTrace[]): StructuredTrace[] {
  // Index: card_id → structured event entry
  const eventByCardId: Record<string, StructuredEvent> = {}
  const result: StructuredTrace[] = []

  // Pointer to the currently "active" interaction group
  let currentEvent: StructuredEvent | undefined

  for (const trace of flat) {
    if (trace.step === 'EVENT') {
      const structured: StructuredEvent = { ...trace, interactions: [], decision_time_ms: null }
      const data = trace.data as Record<string, unknown> | undefined
      const cardId = data?.card_id as string | undefined
      if (cardId) eventByCardId[cardId] = structured
      result.push(structured)
      // Don't change currentEvent here – EVENTs are async / independent
      continue
    }

    if (trace.step === 'ASKFORHELP') {
      // Resolve the parent EVENT via the card id stored in data.id
      const data = trace.data as Record<string, unknown> | undefined
      const cardId = data?.id as string | undefined
      const parent = cardId ? eventByCardId[cardId] : undefined
      if (parent) {
        currentEvent = parent
        currentEvent.interactions.push(trace)
      } else {
        // Orphan ASKFORHELP – keep at top level
        currentEvent = undefined
        result.push(trace)
      }
      continue
    }

    // FEEDBACK / AWARD / anything else → attach to current group if open
    if (currentEvent) {
      currentEvent.interactions.push(trace)
    } else {
      result.push(trace)
    }
  }

  // Compute per-event decision time KPIs
  for (const entry of result) {
    if (isStructuredEvent(entry)) {
      entry.decision_time_ms = computeDecisionTime(entry.interactions)
    }
  }

  return result
}

function escapeCsv(value: unknown): string {
  const normalized = typeof value === 'string' ? value : JSON.stringify(value)
  return `"${(normalized ?? '').replace(/"/g, '""')}"`
}

function buildCsv(session: TraceSession, endedAt: string) {
  const header = [
    'session_id',
    'user_login',
    'session_started_at',
    'session_ended_at',
    'trace_date',
    'use_case',
    'step',
    'data'
  ]

  const rows = session.traces.map((trace) =>
    [
      session.sessionId,
      session.userLogin ?? '',
      session.startedAt,
      endedAt,
      trace.date,
      trace.use_case,
      trace.step,
      trace.data
    ]
      .map((item) => escapeCsv(item))
      .join(',')
  )

  return [header.join(','), ...rows].join('\n')
}

function download(content: string, mimeType: string, fileName: string) {
  const blob = new Blob([content], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = fileName
  document.body.appendChild(anchor)
  anchor.click()
  anchor.remove()
  URL.revokeObjectURL(url)
}

function sessionFileName(session: TraceSession, extension: 'json' | 'csv') {
  const started = session.startedAt.replace(/:/g, '-').replace('.', '-')
  const user = session.userLogin ?? 'unknown'
  return `historic-session-${user}-${started}.${extension}`
}

export function startTraceSession(userLogin?: string) {
  saveSession(createSession(userLogin))
}

export function recordTraceForSession(
  trace: { step: SessionStep; use_case: Trace['use_case']; data: unknown; date?: string }
) {
  const session = loadSession() ?? createSession()

  if (trace.step === 'EVENT') {
    const key = eventKey(trace.data)
    if (key) {
      const alreadyRecorded = session.traces.some(
        (item) => item.step === 'EVENT' && eventKey(item.data) === key
      )
      if (alreadyRecorded) return
    }
  }

  session.traces.push({
    date: trace.date ? String(trace.date) : new Date().toISOString(),
    use_case: trace.use_case,
    step: trace.step,
    data: trace.data
  })
  saveSession(session)
}

export function exportTraceSession(format: ExportFormat = 'json', options: ExportOptions = {}) {
  const force = options.force ?? false
  const session = loadSession() ?? (force ? createSession(options.userLogin) : undefined)
  if (!session) return
  if (!force && session.traces.length === 0) return

  const endedAt = new Date().toISOString()

  if (format === 'csv') {
    const csv = buildCsv(session, endedAt)
    download(csv, 'text/csv;charset=utf-8', sessionFileName(session, 'csv'))
    return
  }

  const structured = buildStructuredTraces(session.traces)

  // --- Session-level KPIs ---
  const totalSessionTimeMs = new Date(endedAt).getTime() - new Date(session.startedAt).getTime()
  const events = structured.filter(isStructuredEvent)
  const totalEvents = events.length
  const sumDecisionTime = events.reduce(
    (sum, evt) => sum + (evt.decision_time_ms ?? 0),
    0
  )
  const kpis: SessionKpis = {
    total_session_time_ms: totalSessionTimeMs,
    avg_decision_time_ms: totalEvents > 0 ? sumDecisionTime / totalEvents : null
  }

  const json = JSON.stringify(
    {
      sessionId: session.sessionId,
      userLogin: session.userLogin,
      startedAt: session.startedAt,
      endedAt,
      kpis,
      traces: structured
    },
    null,
    2
  )
  download(json, 'application/json;charset=utf-8', sessionFileName(session, 'json'))
}

export function clearTraceSession() {
  localStorage.removeItem(STORAGE_KEY)
}
