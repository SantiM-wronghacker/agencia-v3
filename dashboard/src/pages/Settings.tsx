import React from 'react';
import { useAuth } from '../hooks/useAuth';

interface SettingsProps {
  darkMode: boolean;
  onToggleDarkMode: () => void;
}

const Settings: React.FC<SettingsProps> = ({ darkMode, onToggleDarkMode }) => {
  const { isAuthenticated, user, logout } = useAuth();
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8001';

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      <h1 className="text-2xl font-bold">Settings</h1>

      <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 space-y-4">
        <div>
          <h2 className="text-lg font-semibold mb-2">API Configuration</h2>
          <div className="text-sm">
            <span className="text-gray-500 dark:text-gray-400">API URL: </span>
            <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-sm">
              {apiUrl}
            </code>
          </div>
        </div>

        <hr className="border-gray-200 dark:border-gray-700" />

        <div>
          <h2 className="text-lg font-semibold mb-2">Appearance</h2>
          <div className="flex items-center justify-between">
            <span>Dark Mode</span>
            <button
              onClick={onToggleDarkMode}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                darkMode ? 'bg-indigo-600' : 'bg-gray-300'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  darkMode ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        </div>

        <hr className="border-gray-200 dark:border-gray-700" />

        <div>
          <h2 className="text-lg font-semibold mb-2">Authentication</h2>
          <div className="text-sm space-y-1">
            <div>
              <span className="text-gray-500 dark:text-gray-400">Status: </span>
              <span
                className={
                  isAuthenticated
                    ? 'text-green-600 dark:text-green-400'
                    : 'text-red-600 dark:text-red-400'
                }
              >
                {isAuthenticated ? 'Authenticated' : 'Not authenticated'}
              </span>
            </div>
            {user && (
              <div>
                <span className="text-gray-500 dark:text-gray-400">User: </span>
                <span>{user.sub}</span>
                <span className="ml-2 text-xs bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded">
                  {user.role}
                </span>
              </div>
            )}
            {isAuthenticated && (
              <button
                onClick={logout}
                className="mt-2 px-4 py-1.5 text-sm bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-md hover:bg-red-100 dark:hover:bg-red-900/50 transition-colors"
              >
                Logout
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
