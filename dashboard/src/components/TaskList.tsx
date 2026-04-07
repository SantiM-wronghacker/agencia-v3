import React, { useState } from 'react';
import { useTasks, useCancelTask } from '../hooks/useTasks';
import { TaskStatus } from '../types/task';
import TaskCard from './TaskCard';

const statusOptions: (TaskStatus | '')[] = ['', 'pending', 'running', 'completed', 'failed', 'cancelled'];

const TaskList: React.FC = () => {
  const [statusFilter, setStatusFilter] = useState<TaskStatus | ''>('');
  const [search, setSearch] = useState('');

  const { data: tasks, isLoading, error } = useTasks(
    statusFilter || undefined,
    search || undefined
  );
  const cancelMutation = useCancelTask();

  const handleCancel = (id: string) => {
    cancelMutation.mutate(id);
  };

  return (
    <div>
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <input
          type="text"
          placeholder="Search tasks..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
        />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value as TaskStatus | '')}
          className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:ring-2 focus:ring-indigo-500 outline-none"
        >
          {statusOptions.map((s) => (
            <option key={s} value={s}>
              {s || 'All statuses'}
            </option>
          ))}
        </select>
      </div>

      {isLoading && (
        <div className="text-center py-10 text-gray-500">Loading tasks...</div>
      )}

      {error && (
        <div className="text-center py-10 text-red-500">
          Error loading tasks. Please try again.
        </div>
      )}

      {tasks && tasks.length === 0 && (
        <div className="text-center py-10 text-gray-500">
          No tasks found. Create one to get started!
        </div>
      )}

      {tasks && tasks.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} onCancel={handleCancel} />
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;
