import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { getAlerts, AlertsResponse } from '../services/dashboardApi';

const AlertsPanel: React.FC = () => {
  const { data, isLoading } = useQuery<AlertsResponse>({
    queryKey: ['alerts'],
    queryFn: getAlerts,
    refetchInterval: 15_000,
  });

  if (isLoading || !data) {
    return null;
  }

  if (data.alerts.length === 0) {
    return null;
  }

  return (
    <div className="space-y-2">
      {data.alerts.map((alert, idx) => (
        <div
          key={`${alert.type}-${idx}`}
          className={`rounded-lg p-3 border flex items-center space-x-3 ${
            alert.severity === 'warning'
              ? 'bg-yellow-50 dark:bg-yellow-900/30 border-yellow-300 dark:border-yellow-700'
              : 'bg-red-50 dark:bg-red-900/30 border-red-300 dark:border-red-700'
          }`}
        >
          <span className="text-lg">
            {alert.severity === 'warning' ? '⚠️' : '🚨'}
          </span>
          <span className="text-sm font-medium">{alert.message}</span>
        </div>
      ))}
    </div>
  );
};

export default AlertsPanel;
