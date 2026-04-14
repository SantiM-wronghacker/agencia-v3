const API_BASE = process.env.NEXT_PUBLIC_LICENSE_SERVER
const ADMIN_TOKEN = process.env.NEXT_PUBLIC_ADMIN_TOKEN

function adminHeaders(): HeadersInit {
  return {
    'Content-Type': 'application/json',
    'X-Admin-Token': ADMIN_TOKEN ?? '',
  }
}

// ── Clients ───────────────────────────────────────────────────────────────────

export async function getClients() {
  const res = await fetch(`${API_BASE}/clients`, {
    headers: adminHeaders(),
  })
  if (!res.ok) throw new Error(`getClients: ${res.status}`)
  return res.json()
}

export async function createClient(data: {
  name: string
  email: string
  package_type: string
  paid_until: string
  agentes?: string[]
}) {
  const res = await fetch(`${API_BASE}/clients`, {
    method: 'POST',
    headers: adminHeaders(),
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error(`createClient: ${res.status}`)
  return res.json()
}

export async function blockClient(clientId: string) {
  const res = await fetch(`${API_BASE}/clients/${clientId}/block`, {
    method: 'POST',
    headers: adminHeaders(),
  })
  if (!res.ok) throw new Error(`blockClient: ${res.status}`)
  return res.json()
}

export async function unblockClient(clientId: string) {
  const res = await fetch(`${API_BASE}/clients/${clientId}/unblock`, {
    method: 'POST',
    headers: adminHeaders(),
  })
  if (!res.ok) throw new Error(`unblockClient: ${res.status}`)
  return res.json()
}

export async function sendLink(clientId: string) {
  const res = await fetch(`${API_BASE}/clients/${clientId}/send-link`, {
    method: 'POST',
    headers: adminHeaders(),
  })
  if (!res.ok) throw new Error(`sendLink: ${res.status}`)
  return res.json()
}

// ── Validate license (public) ─────────────────────────────────────────────────

export async function validateLicense(licenseKey: string) {
  const res = await fetch(`${API_BASE}/validate/${licenseKey}`)
  if (!res.ok) throw new Error(`validateLicense: ${res.status}`)
  return res.json()
}

// ── Leads (public POST, admin GET) ────────────────────────────────────────────

export async function submitLead(data: {
  nombre: string
  email: string
  mensaje?: string
  plan: string
  agentes: string[]
  precio_estimado?: number
}) {
  const res = await fetch(`${API_BASE}/leads`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error(`submitLead: ${res.status}`)
  return res.json()
}

export async function getLeads() {
  const res = await fetch(`${API_BASE}/leads`, {
    headers: adminHeaders(),
  })
  if (!res.ok) throw new Error(`getLeads: ${res.status}`)
  return res.json()
}
