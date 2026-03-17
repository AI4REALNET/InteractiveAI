import type { Trace } from '@/types/services'

type ExportFormat = 'json' | 'csv'

type StoredTrace = {
  date: string
  use_case: Trace['use_case']
  step: Trace['step']
  data: Trace['data']
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
  trace: Pick<Trace, 'data' | 'step' | 'use_case'> & { date?: string }
) {
  const session = loadSession() ?? createSession()
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

  const json = JSON.stringify(
    {
      sessionId: session.sessionId,
      userLogin: session.userLogin,
      startedAt: session.startedAt,
      endedAt,
      traces: session.traces
    },
    null,
    2
  )
  download(json, 'application/json;charset=utf-8', sessionFileName(session, 'json'))
}

export function clearTraceSession() {
  localStorage.removeItem(STORAGE_KEY)
}
