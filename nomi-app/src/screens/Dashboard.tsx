import Sidebar from '../components/Sidebar'
import StatusBar from '../components/StatusBar'
import AgentCard from '../components/AgentCard'
import AgentRun from './AgentRun'
import Memory from './Memory'
import { Session } from '../lib/store'

interface DashboardProps {
  session: Session
  connected: boolean
  onSuspended: () => void
}

interface DashboardState {
  activeAgent: string | null
  showMemory: boolean
}

import { useState } from 'react'

export default function Dashboard({ session, connected, onSuspended: _onSuspended }: DashboardProps) {
  const [state, setState] = useState<DashboardState>({
    activeAgent: null,
    showMemory: false,
  })

  const handleSelectAgent = (agent: string) => {
    setState({ activeAgent: agent, showMemory: false })
  }

  const handleMemory = () => {
    setState({ activeAgent: null, showMemory: true })
  }

  const handleBack = () => {
    setState({ activeAgent: null, showMemory: false })
  }

  const sidebarActive = state.showMemory
    ? '__memory__'
    : state.activeAgent || ''

  return (
    <div className="flex h-screen bg-nomi-bg overflow-hidden" style={{ fontFamily: 'Outfit, sans-serif' }}>
      <Sidebar
        agentes={session.agentes}
        active={sidebarActive}
        onSelect={handleSelectAgent}
        onMemory={handleMemory}
        plan={session.plan}
        clientName={session.clientName}
      />

      <div className="flex-1 flex flex-col overflow-hidden">
        <main className="flex-1 overflow-y-auto">
          {state.showMemory ? (
            <Memory onBack={handleBack} />
          ) : state.activeAgent ? (
            <AgentRun
              agent={state.activeAgent}
              onBack={handleBack}
              clientId={session.clientId}
            />
          ) : (
            <AgentGrid agentes={session.agentes} onSelect={handleSelectAgent} />
          )}
        </main>

        <StatusBar plan={session.plan} connected={connected} />
      </div>
    </div>
  )
}

function AgentGrid({ agentes, onSelect }: { agentes: string[]; onSelect: (a: string) => void }) {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-nomi-text">Mis agentes</h2>
        <p className="text-nomi-secondary text-sm mt-1">Selecciona un agente para ejecutar una tarea.</p>
      </div>
      <div className="grid grid-cols-2 xl:grid-cols-3 gap-4">
        {agentes.map((agent) => (
          <AgentCard key={agent} agent={agent} onClick={() => onSelect(agent)} />
        ))}
        {agentes.length === 0 && (
          <div className="col-span-3 text-center py-16 text-nomi-secondary">
            No tienes agentes configurados en tu plan.
          </div>
        )}
      </div>
    </div>
  )
}
