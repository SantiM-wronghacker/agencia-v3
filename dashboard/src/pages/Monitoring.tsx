import React from 'react';
import HealthStatus from '../components/HealthStatus';
import MetricsPanel from '../components/MetricsPanel';
import RealtimeUpdates from '../components/RealtimeUpdates';
import { useWebSocket } from '../hooks/useWebSocket';

const Monitoring: React.FC = () => {
  const { isConnected } = useWebSocket();

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      <h1 className="text-2xl font-bold">Monitoring</h1>

      <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
        <h2 className="text-lg font-semibold mb-2">WebSocket Status</h2>
        <div className="flex items-center space-x-2">
          <span
            className={`h-3 w-3 rounded-full ${
              isConnected ? 'bg-green-500' : 'bg-red-500'
            }`}
          />
          <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <HealthStatus />
        <RealtimeUpdates />
      </div>

      <MetricsPanel />
    </div>
  );
};

export default Monitoring;
