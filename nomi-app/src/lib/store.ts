const KEY_LICENSE = 'nomi_license_key'
const KEY_CLIENT_ID = 'nomi_client_id'
const KEY_CLIENT_NAME = 'nomi_client_name'
const KEY_PLAN = 'nomi_plan'
const KEY_AGENTES = 'nomi_agentes'
const KEY_LAST_HB = 'nomi_last_heartbeat'

export interface Session {
  licenseKey: string
  clientId: string
  clientName: string
  plan: string
  agentes: string[]
}

export function saveSession(session: Session): void {
  localStorage.setItem(KEY_LICENSE, session.licenseKey)
  localStorage.setItem(KEY_CLIENT_ID, session.clientId)
  localStorage.setItem(KEY_CLIENT_NAME, session.clientName)
  localStorage.setItem(KEY_PLAN, session.plan)
  localStorage.setItem(KEY_AGENTES, JSON.stringify(session.agentes))
}

export function loadSession(): Session | null {
  const licenseKey = localStorage.getItem(KEY_LICENSE)
  const clientId = localStorage.getItem(KEY_CLIENT_ID)
  if (!licenseKey || !clientId) return null
  return {
    licenseKey,
    clientId,
    clientName: localStorage.getItem(KEY_CLIENT_NAME) || '',
    plan: localStorage.getItem(KEY_PLAN) || 'lite',
    agentes: JSON.parse(localStorage.getItem(KEY_AGENTES) || '[]'),
  }
}

export function clearSession(): void {
  localStorage.removeItem(KEY_LICENSE)
  localStorage.removeItem(KEY_CLIENT_ID)
  localStorage.removeItem(KEY_CLIENT_NAME)
  localStorage.removeItem(KEY_PLAN)
  localStorage.removeItem(KEY_AGENTES)
}

export function saveLastHeartbeat(ts: string): void {
  localStorage.setItem(KEY_LAST_HB, ts)
}

export function loadLastHeartbeat(): string | null {
  return localStorage.getItem(KEY_LAST_HB)
}

// Run history
export interface RunRecord {
  id: string
  agent: string
  task: string
  output: string
  timestamp: string
}

const KEY_RUNS = 'nomi_run_history'

export function saveRun(run: RunRecord): void {
  const history = loadRuns()
  history.unshift(run)
  // Max 50 registros
  localStorage.setItem(KEY_RUNS, JSON.stringify(history.slice(0, 50)))
}

export function loadRuns(): RunRecord[] {
  try {
    return JSON.parse(localStorage.getItem(KEY_RUNS) || '[]')
  } catch {
    return []
  }
}
