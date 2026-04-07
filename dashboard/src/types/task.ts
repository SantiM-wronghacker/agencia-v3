export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';

export interface Task {
  id: string;
  name: string;
  status: TaskStatus;
  description?: string;
  created_at: string;
  updated_at: string;
  result?: unknown;
  logs: string[];
}

export interface TaskCreate {
  name: string;
  description?: string;
}
