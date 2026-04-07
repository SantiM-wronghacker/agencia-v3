import React from 'react';
import { Task, TaskStatus } from '../types/task';

interface TaskCardProps {
  task: Task;
  onCancel?: (id: string) => void;
}

const statusColors: Record<TaskStatus, string> = {
  pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  running: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  completed: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  failed: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  cancelled: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
};

const TaskCard: React.FC<TaskCardProps> = ({ task, onCancel }) => {
  const canCancel = task.status === 'pending' || task.status === 'running';

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow border border-gray-200 dark:border-gray-700">
      <div className="flex items-start justify-between">
        <h3 className="text-lg font-semibold truncate flex-1">{task.name}</h3>
        <span
          className={`ml-2 px-2.5 py-0.5 rounded-full text-xs font-medium ${statusColors[task.status]}`}
        >
          {task.status}
        </span>
      </div>

      {task.description && (
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
          {task.description}
        </p>
      )}

      <div className="mt-3 flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
        <span>Created: {new Date(task.created_at).toLocaleString()}</span>
        <span>Updated: {new Date(task.updated_at).toLocaleString()}</span>
      </div>

      {canCancel && onCancel && (
        <button
          onClick={() => onCancel(task.id)}
          className="mt-3 w-full px-3 py-1.5 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 dark:bg-red-900/30 dark:text-red-400 dark:hover:bg-red-900/50 rounded-md transition-colors"
        >
          Cancel
        </button>
      )}
    </div>
  );
};

export default TaskCard;
