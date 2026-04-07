import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import { getGroups, runGroup, AgentGroup } from '../services/dashboardApi';

const modeBadgeClass: Record<string, string> = {
  pipeline: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  parallel: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
  director: 'bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200',
};

const Groups: React.FC = () => {
  const navigate = useNavigate();
  const [activeGroup, setActiveGroup] = useState<string | null>(null);
  const [task, setTask] = useState('');

  const { data: groups = [], isLoading, error } = useQuery({
    queryKey: ['groups'],
    queryFn: getGroups,
    refetchInterval: 30000,
  });

  const runMutation = useMutation({
    mutationFn: ({ name, task }: { name: string; task: string }) =>
      runGroup(name, task),
    onSuccess: (result) => {
      setActiveGroup(null);
      setTask('');
      navigate(`/groups/${result.group_name}/runs/${result.run_id}`);
    },
  });

  const handleRun = () => {
    if (!activeGroup || !task.trim()) return;
    runMutation.mutate({ name: activeGroup, task: task.trim() });
  };

  const openModal = (name: string) => {
    setActiveGroup(name);
    setTask('');
    runMutation.reset();
  };

  const closeModal = () => {
    setActiveGroup(null);
    setTask('');
    runMutation.reset();
  };

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-gray-500 dark:text-gray-400">Cargando grupos...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-red-500">Error al cargar grupos. ¿Está el servidor corriendo?</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        Grupos de Agentes
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {groups.map((group: AgentGroup) => (
          <div
            key={group.name}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 flex flex-col"
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                {group.name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
              </h2>
              <span
                className={`text-xs font-medium px-2 py-1 rounded-full ${
                  modeBadgeClass[group.mode] ?? 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
                }`}
              >
                {group.mode}
              </span>
            </div>

            {/* Agent chain */}
            <div className="flex flex-wrap items-center gap-1 mb-5 min-h-[2rem]">
              {group.agent_count === 0 ? (
                <span className="text-xs text-gray-400 dark:text-gray-500 italic">
                  Sin agentes configurados
                </span>
              ) : (
                group.agent_roles.map((role, idx) => (
                  <React.Fragment key={role}>
                    <span className="text-xs bg-indigo-50 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-300 px-2 py-1 rounded font-mono">
                      {role}
                    </span>
                    {idx < group.agent_roles.length - 1 && (
                      <span className="text-gray-400 dark:text-gray-500 text-xs">→</span>
                    )}
                  </React.Fragment>
                ))
              )}
            </div>

            {/* Footer */}
            <div className="mt-auto flex items-center justify-between">
              <span className="text-xs text-gray-500 dark:text-gray-400">
                {group.agent_count} agente{group.agent_count !== 1 ? 's' : ''}
              </span>
              <button
                onClick={() => openModal(group.name)}
                disabled={group.agent_count === 0}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white text-sm font-medium rounded-md transition-colors"
              >
                Ejecutar
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {activeGroup && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
          onClick={(e) => e.target === e.currentTarget && closeModal()}
        >
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-lg mx-4 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
              Ejecutar grupo
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              {activeGroup.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
            </p>

            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Tarea
            </label>
            <textarea
              className="w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
              rows={4}
              placeholder="Describe la tarea para el pipeline..."
              value={task}
              onChange={(e) => setTask(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) handleRun();
              }}
              autoFocus
            />

            {runMutation.isError && (
              <p className="mt-2 text-sm text-red-500">
                Error al lanzar el grupo. Verifica que el servidor esté activo.
              </p>
            )}

            <div className="mt-4 flex justify-end gap-3">
              <button
                onClick={closeModal}
                className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-md transition-colors"
              >
                Cancelar
              </button>
              <button
                onClick={handleRun}
                disabled={!task.trim() || runMutation.isPending}
                className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed rounded-md transition-colors flex items-center gap-2"
              >
                {runMutation.isPending ? (
                  <>
                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Lanzando...
                  </>
                ) : (
                  'Confirmar'
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Groups;
