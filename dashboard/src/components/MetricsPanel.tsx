import React from 'react';
import { useMetrics } from '../hooks/useMetrics';

const MetricsPanel: React.FC = () => {
  const { data: metrics, isLoading, error } = useMetrics();

  if (isLoading) {
    return (
      <div className="text-center py-6 text-gray-500">Loading metrics...</div>
    );
  }

  if (error || !metrics) {
    return (
      <div className="text-center py-6 text-red-500">
        Unable to load metrics.
      </div>
    );
  }

  const cards = [
    { label: 'Total Tasks', value: metrics.total_tasks, icon: '📊', color: 'bg-indigo-50 dark:bg-indigo-900/30' },
    { label: 'Completed', value: metrics.completed, icon: '✅', color: 'bg-green-50 dark:bg-green-900/30' },
    { label: 'Failed', value: metrics.failed, icon: '❌', color: 'bg-red-50 dark:bg-red-900/30' },
    { label: 'Pending', value: metrics.pending, icon: '⏳', color: 'bg-yellow-50 dark:bg-yellow-900/30' },
    { label: 'Running', value: metrics.running, icon: '🔄', color: 'bg-blue-50 dark:bg-blue-900/30' },
  ];

  return (
    <div>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
        {cards.map((card) => (
          <div
            key={card.label}
            className={`${card.color} rounded-lg p-4 text-center border border-gray-200 dark:border-gray-700`}
          >
            <div className="text-2xl mb-1">{card.icon}</div>
            <div className="text-2xl font-bold">{card.value}</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              {card.label}
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium">Success Rate</span>
          <span className="text-sm font-bold">
            {metrics.success_rate.toFixed(1)}%
          </span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
          <div
            className="bg-green-500 h-3 rounded-full transition-all duration-500"
            style={{ width: `${metrics.success_rate}%` }}
          />
        </div>
        {metrics.avg_completion_time != null && (
          <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
            Avg. completion time: {metrics.avg_completion_time.toFixed(1)}s
          </div>
        )}
      </div>
    </div>
  );
};

export default MetricsPanel;
