import React, { useState } from 'react';
import TaskList from '../components/TaskList';
import AlertsPanel from '../components/AlertsPanel';
import { useCreateTask } from '../hooks/useTasks';
import { getExportUrl } from '../services/dashboardApi';

const Tasks: React.FC = () => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const createMutation = useCreateTask();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    createMutation.mutate(
      { name: name.trim(), description: description.trim() || undefined },
      {
        onSuccess: () => {
          setName('');
          setDescription('');
        },
      }
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Tasks</h1>
        <div className="flex space-x-2">
          <a
            href={getExportUrl('csv')}
            download="tasks.csv"
            className="px-4 py-2 text-sm bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors"
          >
            Export CSV
          </a>
          <a
            href={getExportUrl('json')}
            download="tasks.json"
            className="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
          >
            Export JSON
          </a>
        </div>
      </div>

      <AlertsPanel />

      <form
        onSubmit={handleSubmit}
        className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 space-y-3"
      >
        <h2 className="text-lg font-semibold">Create Task</h2>
        <input
          type="text"
          placeholder="Task name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
        />
        <textarea
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none resize-none"
        />
        <button
          type="submit"
          disabled={createMutation.isPending}
          className="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
        >
          {createMutation.isPending ? 'Creating...' : 'Create Task'}
        </button>
      </form>

      <TaskList />
    </div>
  );
};

export default Tasks;
