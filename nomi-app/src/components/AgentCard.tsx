const AGENT_DESCRIPTIONS: Record<string, string> = {
  content_pipeline: 'Genera contenido SEO completo: investiga, escribe y optimiza.',
  business_analysis: 'Analiza tu negocio y genera reportes estratégicos.',
  legal_review: 'Revisa documentos legales y evalúa riesgos.',
  ops_automation: 'Automatiza y optimiza tus procesos operativos.',
  social_media_manager: 'Gestiona y publica en todas tus redes sociales.',
  email_campaign: 'Crea y envía campañas de email marketing.',
  sales_pipeline: 'Gestiona leads y cierra más ventas.',
  quotation_generator: 'Genera cotizaciones profesionales en segundos.',
  hr_onboarding: 'Automatiza el onboarding de nuevos empleados.',
  accounting_report: 'Genera reportes contables y fiscales.',
  ops_daily: 'Revisa y delega las tareas del día.',
  blog_publisher: 'Escribe y publica posts en tu blog.',
  content_repurposer: 'Convierte un contenido en múltiples formatos.',
  restaurant_manager: 'Gestiona menú, reservas y contenido.',
  health_assistant: 'Gestiona citas y comunicación con pacientes.',
  real_estate_agent: 'Publica propiedades y da seguimiento a leads.',
  logistics_coordinator: 'Coordina envíos y rastrea paquetes.',
  insurance_advisor: 'Asesora sobre pólizas y renueva clientes.',
  travel_planner: 'Crea itinerarios y paquetes de viaje.',
  market_intelligence: 'Analiza competidores e identifica oportunidades.',
  financial_advisor: 'Analiza datos financieros y hace recomendaciones.',
  education_manager: 'Gestiona cursos, quizzes y progreso de alumnos.',
  daily_report: 'Genera el reporte diario de tu negocio.',
  social_autopilot: 'Publica automáticamente en redes sociales.',
  lead_nurturing: 'Nutre y califica leads de forma automática.',
}

const AGENT_ICONS: Record<string, string> = {
  content_pipeline: '✍️',
  business_analysis: '📊',
  legal_review: '⚖️',
  ops_automation: '⚙️',
  social_media_manager: '📱',
  email_campaign: '📧',
  sales_pipeline: '💼',
  quotation_generator: '📄',
  hr_onboarding: '👥',
  accounting_report: '🧾',
  ops_daily: '📋',
  blog_publisher: '📝',
  content_repurposer: '♻️',
  restaurant_manager: '🍽️',
  health_assistant: '🏥',
  real_estate_agent: '🏠',
  logistics_coordinator: '🚚',
  insurance_advisor: '🛡️',
  travel_planner: '✈️',
  market_intelligence: '🔍',
  financial_advisor: '💰',
  education_manager: '🎓',
  daily_report: '📈',
  social_autopilot: '🤖',
  lead_nurturing: '🎯',
}

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

interface AgentCardProps {
  agent: string
  onClick: () => void
}

export default function AgentCard({ agent, onClick }: AgentCardProps) {
  return (
    <button
      onClick={onClick}
      className="text-left p-5 rounded-xl border border-nomi-border hover:border-nomi-accent/50 hover:bg-white/60 transition-all duration-150"
      style={{ background: 'rgba(255,255,255,0.35)' }}
    >
      <div className="text-3xl mb-3">{AGENT_ICONS[agent] || '🤖'}</div>
      <div className="font-semibold text-nomi-text mb-1">
        {AGENT_LABELS[agent] || agent}
      </div>
      <div className="text-xs text-nomi-secondary leading-relaxed">
        {AGENT_DESCRIPTIONS[agent] || 'Agente de automatización.'}
      </div>
    </button>
  )
}
