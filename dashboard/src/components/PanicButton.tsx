import React from 'react';
import { useTasks, useCancelTask } from '../hooks/useTasks';

const PanicButton: React.FC = () => {
  const { data: tasks } = useTasks();
  const cancelMutation = useCancelTask();

  const handlePanic = () => {
    const confirmed = window.confirm(
      '⚠️ EMERGENCY STOP\n\nThis will cancel ALL pending and running tasks.\n\nAre you sure?'
    );
    if (!confirmed) return;

    const activeTasks = tasks?.filter(
      (t) => t.status === 'pending' || t.status === 'running'
    );
    activeTasks?.forEach((t) => cancelMutation.mutate(t.id));
  };

  const activeCount =
    tasks?.filter((t) => t.status === 'pending' || t.status === 'running')
      .length ?? 0;

  return (
    <button
      onClick={handlePanic}
      disabled={activeCount === 0}
      className={`relative px-6 py-3 rounded-lg font-bold text-white transition-all ${
        activeCount > 0
          ? 'bg-red-600 hover:bg-red-700 animate-pulse shadow-lg shadow-red-500/50'
          : 'bg-gray-400 cursor-not-allowed'
      }`}
    >
      🚨 EMERGENCY STOP
      {activeCount > 0 && (
        <span className="ml-2 bg-white text-red-600 text-xs px-2 py-0.5 rounded-full">
          {activeCount}
        </span>
      )}
    </button>
  );
};

export default PanicButton;
