import api from './api';
import { Task, TaskCreate } from '../types/task';
import { DashboardMetrics, HealthResponse } from '../types/metrics';

const BASE = '/api/v2/dashboard';

export async function getHealth(): Promise<HealthResponse> {
  const { data } = await api.get<HealthResponse>(`${BASE}/health`);
  return data;
}

export async function getMetrics(): Promise<DashboardMetrics> {
  const { data } = await api.get<DashboardMetrics>(`${BASE}/metrics`);
  return data;
}

export async function getTasks(params?: {
  status?: string;
  search?: string;
}): Promise<Task[]> {
  const { data } = await api.get<Task[]>(`${BASE}/tasks`, { params });
  return data;
}

export async function getTask(id: string): Promise<Task> {
  const { data } = await api.get<Task>(`${BASE}/tasks/${id}`);
  return data;
}

export async function createTask(taskData: TaskCreate): Promise<Task> {
  const { data } = await api.post<Task>(`${BASE}/tasks`, taskData);
  return data;
}

export async function cancelTask(id: string): Promise<Task> {
  const { data } = await api.post<Task>(`${BASE}/tasks/${id}/cancel`);
  return data;
}

export async function getTaskLogs(id: string): Promise<string[]> {
  const { data } = await api.get<string[]>(`${BASE}/tasks/${id}/logs`);
  return data;
}

export interface AlertConfig {
  max_failed: number;
  min_success_rate: number;
}

export interface Alert {
  type: string;
  severity: string;
  message: string;
}

export interface AlertsResponse {
  alerts: Alert[];
  config: AlertConfig;
}

export async function getAlerts(): Promise<AlertsResponse> {
  const { data } = await api.get<AlertsResponse>(`${BASE}/alerts`);
  return data;
}

export async function getAlertConfig(): Promise<AlertConfig> {
  const { data } = await api.get<AlertConfig>(`${BASE}/alerts/config`);
  return data;
}

export async function updateAlertConfig(config: AlertConfig): Promise<AlertConfig> {
  const { data } = await api.put<AlertConfig>(`${BASE}/alerts/config`, config);
  return data;
}

export function getExportUrl(format: 'csv' | 'json'): string {
  const baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8001';
  return `${baseUrl}${BASE}/tasks/export?format=${format}`;
}

// ---------------------------------------------------------------------------
// v3 — Grupos, runs y memoria
// ---------------------------------------------------------------------------

export interface AgentGroup {
  name: string;
  mode: string;
  agent_count: number;
  agent_roles: string[];
}

export interface RunStep {
  id: string;
  run_id: string;
  step_index: number;
  agent_role: string;
  input: string;
  output: string | null;
  provider: string | null;
  duration_ms: number | null;
  success: number;
  error: string | null;
  timestamp: string;
}

export interface GroupRun {
  id: string;
  group_name: string;
  mode: string | null;
  status: string;
  input_summary: string | null;
  final_output: string | null;
  total_duration_ms: number | null;
  success: number | null;
  error: string | null;
  created_at: string;
  completed_at: string | null;
  steps: RunStep[];
}

export interface MemoryResult {
  content: string;
  run_id: string;
  timestamp: string;
  agent_role: string;
  group_name: string;
}

export async function getGroups(): Promise<AgentGroup[]> {
  const { data } = await api.get<AgentGroup[]>('/groups');
  return data;
}

export async function runGroup(
  name: string,
  task: string
): Promise<{ run_id: string; status: string; group_name: string }> {
  const { data } = await api.post(`/groups/${name}/run`, { task });
  return data;
}

export async function getGroupRun(name: string, runId: string): Promise<GroupRun> {
  const { data } = await api.get<GroupRun>(`/groups/${name}/runs/${runId}`);
  return data;
}

export async function searchMemory(q: string, limit = 10): Promise<MemoryResult[]> {
  const { data } = await api.get<MemoryResult[]>('/memory/search', {
    params: { q, limit },
  });
  return data;
}
