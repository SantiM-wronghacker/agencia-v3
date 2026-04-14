import { loadRuns, RunRecord } from '../lib/store'

const AGENT_LABELS: Record<string, string> = {
  content_pipeline: 'Content Pipeline',
  business_analysis: 'Business Analysis',
  legal_review: 'Legal Review',
  ops_automation: 'Ops Automation',
  social_media_manager: 'Social Media',
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
  market_intelligence: 'Inteligencia',
  financial_advisor: 'Finanzas',
  education_manager: 'Educación',
  daily_report: 'Reporte Diario',
  social_autopilot: 'Autopiloto Social',
  lead_nurturing: 'Lead Nurturing',
}

interface MemoryProps {
  onBack: () => void
}

export default function Memory({ onBack }: MemoryProps) {
  const runs = loadRuns()
  const [selected, setSelected] = useState<RunRecord | null>(null)

  return (
    <div className="p-8">
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={onBack}
          className="text-nomi-secondary hover:text-nomi-text transition-colors text-sm"
        >
          ← Volver
        </button>
        <h2 className="text-xl font-semibold text-nomi-text">Historial de tareas</h2>
      </div>

      {runs.length === 0 ? (
        <div className="text-center py-16 text-nomi-secondary">
          <div className="text-4xl mb-4">📭</div>
          <p>Aún no hay tareas ejecutadas.</p>
        </div>
      ) : (
        <div className="grid gap-3">
          {runs.map((run) => (
            <button
              key={run.id}
              onClick={() => setSelected(selected?.id === run.id ? null : run)}
              className="text-left p-4 rounded-xl border border-nomi-border hover:border-nomi-accent/40 transition-all duration-150"
              style={{ background: 'rgba(255,255,255,0.4)' }}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium mb-1">
                    {AGENT_LABELS[run.agent] || run.agent}
                  </div>
                  <div className="text-xs text-nomi-secondary truncate">{run.task}</div>
                </div>
                <div className="text-xs text-nomi-secondary flex-shrink-0">
                  {new Date(run.timestamp).toLocaleString('es-MX', {
                    dateStyle: 'short',
                    timeStyle: 'short',
                  })}
                </div>
              </div>

              {selected?.id === run.id && (
                <div className="mt-3 pt-3 border-t border-nomi-border">
                  <pre className="text-xs text-nomi-text whitespace-pre-wrap leading-relaxed max-h-48 overflow-y-auto">
                    {run.output || 'Sin output guardado'}
                  </pre>
                </div>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

import { useState } from 'react'
