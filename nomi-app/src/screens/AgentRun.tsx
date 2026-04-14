import { useState, useRef, useEffect } from 'react'
import { runAgent, connectAgentWS, AGENCIA_URL } from '../lib/api'
import { saveRun } from '../lib/store'

const AGENT_LABELS: Record<string, string> = {
  content_pipeline: 'Content Pipeline',
  business_analysis: 'Business Analysis',
  legal_review: 'Legal Review',
  ops_automation: 'Ops Automation',
  social_media_manager: 'Social Media Manager',
  email_campaign: 'Email Campaign',
  sales_pipeline: 'Sales Pipeline',
  quotation_generator: 'Cotizaciones',
  hr_onboarding: 'HR Onboarding',
  accounting_report: 'Contabilidad',
  ops_daily: 'Ops Diarias',
  blog_publisher: 'Blog Publisher',
  content_repurposer: 'Content Repurposer',
  restaurant_manager: 'Restaurante',
  health_assistant: 'Salud',
  real_estate_agent: 'Bienes Raíces',
  logistics_coordinator: 'Logística',
  insurance_advisor: 'Seguros',
  travel_planner: 'Viajes',
  market_intelligence: 'Inteligencia de Mercado',
  financial_advisor: 'Asesor Financiero',
  education_manager: 'Educación',
  daily_report: 'Reporte Diario',
  social_autopilot: 'Autopiloto Social',
  lead_nurturing: 'Lead Nurturing',
}

interface AgentRunProps {
  agent: string
  onBack: () => void
  clientId: string
}

type RunStatus = 'idle' | 'running' | 'done' | 'error'

export default function AgentRun({ agent, onBack }: AgentRunProps) {
  const [task, setTask] = useState('')
  const [output, setOutput] = useState('')
  const [status, setStatus] = useState<RunStatus>('idle')
  const [error, setError] = useState('')
  const outputRef = useRef<HTMLTextAreaElement>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const fullOutputRef = useRef('')

  // Scroll output automático
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight
    }
  }, [output])

  // Cleanup websocket on unmount
  useEffect(() => {
    return () => {
      wsRef.current?.close()
    }
  }, [])

  const handleRun = async () => {
    if (!task.trim() || status === 'running') return
    setError('')
    setOutput('')
    fullOutputRef.current = ''
    setStatus('running')

    try {
      // Intenta WebSocket primero para output en tiempo real
      const wsBase = AGENCIA_URL.replace(/^http/, 'ws')
      const ws = new WebSocket(`${wsBase}/ws/groups/${agent}/run`)
      wsRef.current = ws

      let wsWorked = false

      ws.onopen = () => {
        wsWorked = true
        ws.send(JSON.stringify({ task: task.trim() }))
      }

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data)
          if (msg.type === 'done') {
            setStatus('done')
            saveRunRecord()
            ws.close()
          } else if (msg.content || msg.output) {
            const chunk = msg.content || msg.output || ''
            fullOutputRef.current += chunk
            setOutput(fullOutputRef.current)
          } else if (msg.error) {
            setError(msg.error)
            setStatus('error')
            ws.close()
          }
        } catch {
          // Texto plano
          fullOutputRef.current += event.data
          setOutput(fullOutputRef.current)
        }
      }

      ws.onerror = async () => {
        if (!wsWorked) {
          // Fallback a REST
          ws.close()
          await runViaRest()
        }
      }

      ws.onclose = () => {
        // onclose se llama después de que el state ya puede haber cambiado;
        // sólo completamos si nadie más lo hizo
        setStatus((prev) => prev === 'running' ? 'done' : prev)
      }

    } catch {
      await runViaRest()
    }
  }

  const runViaRest = async () => {
    try {
      const runId = await runAgent(agent, task.trim())
      // Polling del resultado
      let attempts = 0
      const poll = setInterval(async () => {
        try {
          const result = await fetch(`${AGENCIA_URL}/groups/${agent}/runs/${runId}`)
          const data = await result.json()
          if (data.output) {
            fullOutputRef.current = data.output
            setOutput(data.output)
          }
          if (data.status === 'done' || data.status === 'completed' || attempts > 60) {
            clearInterval(poll)
            setStatus('done')
            saveRunRecord()
          }
          attempts++
        } catch {
          clearInterval(poll)
          setStatus('done')
        }
      }, 2000)
    } catch (err) {
      setError('No se pudo conectar con el servidor de agencia. ¿Está corriendo agencia-v3?')
      setStatus('error')
    }
  }

  const saveRunRecord = () => {
    saveRun({
      id: Date.now().toString(),
      agent,
      task: task.trim(),
      output: fullOutputRef.current,
      timestamp: new Date().toISOString(),
    })
  }

  const handleStop = () => {
    wsRef.current?.close()
    setStatus('done')
  }

  return (
    <div className="p-8 h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={onBack}
          className="text-nomi-secondary hover:text-nomi-text transition-colors text-sm flex items-center gap-1"
        >
          ← Volver
        </button>
        <h2 className="text-xl font-semibold text-nomi-text">
          {AGENT_LABELS[agent] || agent}
        </h2>
        {status === 'running' && (
          <span className="text-xs px-2 py-0.5 rounded-full bg-nomi-accent/20 text-nomi-accent font-medium animate-pulse">
            Ejecutando...
          </span>
        )}
        {status === 'done' && (
          <span className="text-xs px-2 py-0.5 rounded-full bg-green-100 text-green-700 font-medium">
            Completado
          </span>
        )}
      </div>

      {/* Task input */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Descripción de la tarea</label>
        <textarea
          value={task}
          onChange={(e) => setTask(e.target.value)}
          disabled={status === 'running'}
          className="w-full px-4 py-3 rounded-xl border border-nomi-border bg-white/60 focus:outline-none focus:border-nomi-accent text-sm resize-none disabled:opacity-60"
          rows={3}
          placeholder={`Describe qué quieres que haga ${AGENT_LABELS[agent] || 'el agente'}...`}
        />
      </div>

      {/* Controls */}
      <div className="flex gap-3 mb-6">
        <button
          onClick={handleRun}
          disabled={!task.trim() || status === 'running'}
          className="px-6 py-2 bg-nomi-accent text-white rounded-lg font-medium text-sm hover:brightness-90 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {status === 'running' ? 'Ejecutando...' : 'Ejecutar'}
        </button>
        {status === 'running' && (
          <button
            onClick={handleStop}
            className="px-6 py-2 border border-nomi-border rounded-lg font-medium text-sm hover:bg-white/40"
          >
            Detener
          </button>
        )}
        {(status === 'done' || status === 'error') && (
          <button
            onClick={() => { setOutput(''); setStatus('idle'); fullOutputRef.current = '' }}
            className="px-6 py-2 border border-nomi-border rounded-lg font-medium text-sm hover:bg-white/40"
          >
            Nueva tarea
          </button>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="mb-4 text-sm text-red-600 bg-red-50 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {/* Output */}
      {(output || status === 'running') && (
        <div className="flex-1 flex flex-col min-h-0">
          <label className="block text-sm font-medium mb-2">Resultado</label>
          <textarea
            ref={outputRef}
            readOnly
            value={output || (status === 'running' ? 'Procesando...' : '')}
            className="flex-1 px-4 py-3 rounded-xl border border-nomi-border bg-white/40 text-sm resize-none font-mono leading-relaxed min-h-48"
          />
        </div>
      )}
    </div>
  )
}
