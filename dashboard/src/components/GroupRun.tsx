import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getGroupRun, GroupRun as GroupRunType, RunStep } from '../services/dashboardApi';

function stepStatus(step: RunStep): 'done' | 'failed' | 'pending' {
  if (step.success === 1) return 'done';
  if (step.error) return 'failed';
  return 'pending';
}

const statusBadge: Record<string, string> = {
  running:   'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300',
  completed: 'bg-green-100  text-green-800  dark:bg-green-900/40  dark:text-green-300',
  failed:    'bg-red-100    text-red-800    dark:bg-red-900/40    dark:text-red-300',
};

const stepBadge: Record<string, string> = {
  done:    'bg-green-500',
  failed:  'bg-red-500',
  pending: 'bg-gray-300 dark:bg-gray-600',
};

const StepRow: React.FC<{ step: RunStep; isLast: boolean }> = ({ step, isLast }) => {
  const [expanded, setExpanded] = useState(false);
  const status = stepStatus(step);

  return (
    <div className="relative flex gap-4">
      {/* Timeline line */}
      {!isLast && (
        <div className="absolute left-[11px] top-6 bottom-0 w-0.5 bg-gray-200 dark:bg-gray-700" />
      )}

      {/* Dot */}
      <div
        className={`mt-1 w-6 h-6 rounded-full flex-shrink-0 flex items-center justify-center ${stepBadge[status]}`}
      >
        {status === 'done'   && <span className="text-white text-xs">✓</span>}
        {status === 'failed' && <span className="text-white text-xs">✗</span>}
        {status === 'pending' && <span className="text-xs text-gray-400">·</span>}
      </div>

      {/* Content */}
      <div className="flex-1 pb-6">
        <div className="flex flex-wrap items-center gap-2 mb-1">
          <span className="font-mono text-sm font-medium text-gray-900 dark:text-white">
            {step.agent_role}
          </span>
          <span
            className={`text-xs px-2 py-0.5 rounded-full ${
              status === 'done'    ? 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300' :
              status === 'failed'  ? 'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300' :
                                    'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400'
            }`}
          >
            {status}
          </span>
          {step.duration_ms !== null && (
            <span className="text-xs text-gray-400 dark:text-gray-500">
              {step.duration_ms}ms
            </span>
          )}
          {step.provider && (
            <span className="text-xs text-indigo-500 dark:text-indigo-400">
              {step.provider}
            </span>
          )}
        </div>

        {step.error && (
          <p className="text-xs text-red-500 mt-1">{step.error}</p>
        )}

        {step.output && (
          <div className="mt-2">
            <button
              onClick={() => setExpanded((v) => !v)}
              className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1"
            >
              {expanded ? '▾ Ocultar output' : '▸ Ver output'}
            </button>
            {expanded && (
              <pre className="mt-2 text-xs bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded p-3 whitespace-pre-wrap break-words max-h-48 overflow-y-auto">
                {step.output}
              </pre>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

const GroupRun: React.FC = () => {
  const { name, run_id } = useParams<{ name: string; run_id: string }>();

  const { data: run, isLoading, error } = useQuery<GroupRunType>({
    queryKey: ['groupRun', name, run_id],
    queryFn: () => getGroupRun(name!, run_id!),
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      if (status === 'completed' || status === 'failed') return false;
      return 2000;
    },
    enabled: !!name && !!run_id,
  });

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-gray-500 dark:text-gray-400">Cargando run...</div>
      </div>
    );
  }

  if (error || !run) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-red-500">Run no encontrado.</div>
        <Link to="/groups" className="text-indigo-600 dark:text-indigo-400 text-sm hover:underline mt-2 inline-block">
          ← Volver a Grupos
        </Link>
      </div>
    );
  }

  const isFinished = run.status === 'completed' || run.status === 'failed';

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Breadcrumb */}
      <Link
        to="/groups"
        className="text-sm text-indigo-600 dark:text-indigo-400 hover:underline mb-4 inline-block"
      >
        ← Grupos
      </Link>

      {/* Header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">
              {run.group_name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
            </h1>
            <p className="text-sm text-gray-500 dark:text-gray-400 font-mono mt-1">
              {run_id?.slice(0, 8)}...
            </p>
          </div>
          <div className="flex items-center gap-3">
            {!isFinished && (
              <span className="flex items-center gap-1.5 text-xs text-yellow-600 dark:text-yellow-400">
                <span className="w-2 h-2 rounded-full bg-yellow-500 animate-pulse" />
                Actualizando...
              </span>
            )}
            <span
              className={`text-sm font-medium px-3 py-1 rounded-full ${
                statusBadge[run.status] ?? 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
              }`}
            >
              {run.status}
            </span>
          </div>
        </div>

        {run.input_summary && (
          <p className="mt-3 text-sm text-gray-600 dark:text-gray-300 bg-gray-50 dark:bg-gray-900/50 rounded px-3 py-2">
            {run.input_summary}
          </p>
        )}

        {run.total_duration_ms !== null && (
          <p className="mt-2 text-xs text-gray-400 dark:text-gray-500">
            Duración total: {run.total_duration_ms}ms
          </p>
        )}
      </div>

      {/* Steps timeline */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-base font-semibold text-gray-900 dark:text-white mb-5">Steps</h2>
        {run.steps.length === 0 ? (
          <p className="text-sm text-gray-400 dark:text-gray-500 italic">
            Esperando steps...
          </p>
        ) : (
          <div>
            {run.steps
              .slice()
              .sort((a, b) => a.step_index - b.step_index)
              .map((step, idx) => (
                <StepRow
                  key={step.id ?? `${step.step_index}`}
                  step={step}
                  isLast={idx === run.steps.length - 1}
                />
              ))}
          </div>
        )}
      </div>

      {/* Final output */}
      {run.status === 'completed' && run.final_output && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border-l-4 border-green-500">
          <h2 className="text-base font-semibold text-gray-900 dark:text-white mb-3">
            ✅ Output final
          </h2>
          <pre className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap break-words">
            {run.final_output}
          </pre>
        </div>
      )}

      {run.status === 'failed' && run.error && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border-l-4 border-red-500">
          <h2 className="text-base font-semibold text-red-600 dark:text-red-400 mb-2">
            ❌ Error
          </h2>
          <p className="text-sm text-gray-700 dark:text-gray-300">{run.error}</p>
        </div>
      )}
    </div>
  );
};

export default GroupRun;
