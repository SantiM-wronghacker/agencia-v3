export interface DashboardMetrics {
  total_tasks: number;
  completed: number;
  failed: number;
  pending: number;
  running: number;
  success_rate: number;
  avg_completion_time?: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  uptime: number;
  services: Record<string, string>;
}
