interface SidebarProps {
  agentes: string[]
  active: string
  onSelect: (agent: string) => void
  onMemory: () => void
  plan: string
  clientName: string
}

// Mapa de agente_key → nombre display
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

export default function Sidebar({ agentes, active, onSelect, onMemory, plan, clientName }: SidebarProps) {
  return (
    <aside style={{ background: 'rgba(255,255,255,0.4)', borderRight: '1px solid #ddd8ce' }}
      className="w-56 flex-shrink-0 flex flex-col h-full">
      {/* Logo */}
      <div className="px-5 py-5 border-b border-nomi-border">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" style={{ height: 28, width: 28 }}>
          <rect width="32" height="32" rx="7" fill="#6aaad9"/>
          <text x="16" y="16" textAnchor="middle" dominantBaseline="central"
            fontFamily="'Helvetica Neue',Helvetica,Arial,sans-serif"
            fontSize="22" fontWeight="700" fill="white">n</text>
        </svg>
        <div className="text-xs text-nomi-secondary mt-0.5 truncate">{clientName}</div>
      </div>

      {/* Agentes */}
      <nav className="flex-1 overflow-y-auto py-3 px-2">
        <div className="text-xs text-nomi-secondary uppercase tracking-wider px-3 mb-2">
          Mis agentes
        </div>
        {agentes.map((agent) => (
          <button
            key={agent}
            onClick={() => onSelect(agent)}
            className={`w-full text-left px-3 py-2 rounded-lg text-sm mb-0.5 transition-all duration-150
              ${active === agent
                ? 'bg-nomi-accent/20 text-nomi-accent font-medium'
                : 'text-nomi-text hover:bg-white/60'
              }`}
          >
            {AGENT_LABELS[agent] || agent}
          </button>
        ))}
      </nav>

      {/* Memory + plan */}
      <div className="border-t border-nomi-border p-2">
        <button
          onClick={onMemory}
          className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-all duration-150
            ${active === '__memory__'
              ? 'bg-nomi-accent/20 text-nomi-accent font-medium'
              : 'text-nomi-secondary hover:bg-white/60'
            }`}
        >
          Historial
        </button>
        <div className="px-3 py-2 mt-1">
          <span className="text-xs px-2 py-0.5 rounded-full bg-nomi-accent/10 text-nomi-accent font-medium capitalize">
            {plan}
          </span>
        </div>
      </div>
    </aside>
  )
}
