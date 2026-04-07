import React from 'react';
import { useHealth } from '../hooks/useMetrics';

const HealthStatus: React.FC = () => {
  const { data: health, isLoading, error } = useHealth();

  if (isLoading) {
    return (
      <div className="text-center py-6 text-gray-500">
        Checking health...
      </div>
    );
  }

  if (error || !health) {
    return (
      <div className="bg-red-50 dark:bg-red-900/30 rounded-lg p-4 border border-red-200 dark:border-red-700">
        <div className="flex items-center space-x-2">
          <span className="h-3 w-3 bg-red-500 rounded-full" />
          <span className="font-medium text-red-700 dark:text-red-300">
            API Offline
          </span>
        </div>
      </div>
    );
  }

  const isUp = health.status === 'ok' || health.status === 'healthy';

  const formatUptime = (seconds: number): string => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    return `${h}h ${m}m`;
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <span
            className={`h-3 w-3 rounded-full ${isUp ? 'bg-green-500' : 'bg-red-500'}`}
          />
          <span className="font-medium">
            API {isUp ? 'Online' : 'Degraded'}
          </span>
        </div>
        <span className="text-sm text-gray-500 dark:text-gray-400">
          v{health.version}
        </span>
      </div>

      <div className="text-sm text-gray-600 dark:text-gray-400 mb-3">
        Uptime: {formatUptime(health.uptime)}
      </div>

      {Object.keys(health.services).length > 0 && (
        <div>
          <h4 className="text-sm font-medium mb-2">Services</h4>
          <div className="space-y-1">
            {Object.entries(health.services).map(([name, status]) => {
              const ok =
                status === 'ok' || status === 'healthy' || status === 'up';
              return (
                <div
                  key={name}
                  className="flex items-center justify-between text-sm"
                >
                  <span className="capitalize">{name}</span>
                  <span className="flex items-center space-x-1">
                    <span
                      className={`h-2 w-2 rounded-full ${ok ? 'bg-green-500' : 'bg-red-500'}`}
                    />
                    <span
                      className={ok ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}
                    >
                      {status}
                    </span>
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default HealthStatus;
