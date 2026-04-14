const LICENSE_SERVER = import.meta.env.VITE_LICENSE_SERVER || 'http://localhost:8080'
export const AGENCIA_URL = import.meta.env.VITE_AGENCIA_URL || 'http://localhost:8001'

export interface ValidateResponse {
  valid: boolean
  status: string
  client_name?: string
  plan?: string
  agentes?: string[]
  message?: string
}

export interface HeartbeatResponse {
  active: boolean
  status: string
  message: string
  days_remaining: number
  hours_offline: number
}

export async function validateLicense(licenseKey: string): Promise<ValidateResponse> {
  const res = await fetch(`${LICENSE_SERVER}/validate/${licenseKey}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export async function sendHeartbeat(
  clientId: string,
  licenseKey: string,
  packageType: string,
): Promise<HeartbeatResponse> {
  const res = await fetch(`${LICENSE_SERVER}/heartbeat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: clientId,
      license_key: licenseKey,
      package_type: packageType,
      timestamp: new Date().toISOString(),
    }),
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export async function runAgent(
  groupName: string,
  task: string,
): Promise<string> {
  const res = await fetch(`${AGENCIA_URL}/groups/${groupName}/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task }),
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  const data = await res.json()
  return data.run_id as string
}

export async function getRunResult(groupName: string, runId: string) {
  const res = await fetch(`${AGENCIA_URL}/groups/${groupName}/runs/${runId}`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export function connectAgentWS(
  groupName: string,
  runId: string,
  onMessage: (data: string) => void,
  onDone: () => void,
): WebSocket {
  const wsBase = (AGENCIA_URL).replace(/^http/, 'ws')
  const ws = new WebSocket(`${wsBase}/ws/groups/${groupName}/runs/${runId}`)

  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data)
      if (msg.type === 'done') {
        onDone()
      } else if (msg.content) {
        onMessage(msg.content)
      } else {
        onMessage(event.data)
      }
    } catch {
      onMessage(event.data)
    }
  }

  ws.onerror = () => onDone()
  ws.onclose = () => onDone()

  return ws
}
