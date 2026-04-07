import React from 'react';
import MetricsPanel from '../components/MetricsPanel';
import HealthStatus from '../components/HealthStatus';
import RealtimeUpdates from '../components/RealtimeUpdates';
import AlertsPanel from '../components/AlertsPanel';
import PanicButton from '../components/PanicButton';
import TaskCard from '../components/TaskCard';
import { useTasks, useCancelTask } from '../hooks/useTasks';

const Dashboard: React.FC = () => {
  const { data: tasks } = useTasks();
  const cancelMutation = useCancelTask();
  const recentTasks = tasks?.slice(0, 5) ?? [];

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <PanicButton />
      </div>

      <AlertsPanel />

      <MetricsPanel />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <HealthStatus />
        <RealtimeUpdates />
      </div>

      <div>
        <h2 className="text-lg font-semibold mb-3">Recent Tasks</h2>
        {recentTasks.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400">No tasks yet.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {recentTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onCancel={(id) => cancelMutation.mutate(id)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
