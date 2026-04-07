import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Tasks from './pages/Tasks';
import Monitoring from './pages/Monitoring';
import Settings from './pages/Settings';
import Groups from './components/Groups';
import GroupRun from './components/GroupRun';
import Memory from './components/Memory';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      staleTime: 5000,
    },
  },
});

const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState<boolean>(() => {
    const stored = localStorage.getItem('darkMode');
    return stored ? stored === 'true' : true;
  });

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('darkMode', String(darkMode));
  }, [darkMode]);

  const toggleDarkMode = () => setDarkMode((prev) => !prev);

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
        <Navbar darkMode={darkMode} onToggleDarkMode={toggleDarkMode} />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/tasks" element={<Tasks />} />
          <Route path="/monitoring" element={<Monitoring />} />
          <Route
            path="/settings"
            element={
              <Settings
                darkMode={darkMode}
                onToggleDarkMode={toggleDarkMode}
              />
            }
          />
          <Route path="/groups" element={<Groups />} />
          <Route path="/groups/:name/runs/:run_id" element={<GroupRun />} />
          <Route path="/memory" element={<Memory />} />
        </Routes>
      </div>
    </QueryClientProvider>
  );
};

export default App;
