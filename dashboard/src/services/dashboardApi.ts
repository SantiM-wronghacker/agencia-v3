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
