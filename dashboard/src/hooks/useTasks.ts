import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getTasks, getTask, createTask, cancelTask } from '../services/dashboardApi';
import { TaskCreate, TaskStatus } from '../types/task';

const POLLING_INTERVAL = 10_000; // 10 seconds fallback polling

export function useTasks(status?: TaskStatus, search?: string) {
  return useQuery({
    queryKey: ['tasks', status, search],
    queryFn: () =>
      getTasks({
        status: status || undefined,
        search: search || undefined,
      }),
    refetchInterval: POLLING_INTERVAL,
  });
}

export function useTask(taskId: string) {
  return useQuery({
    queryKey: ['task', taskId],
    queryFn: () => getTask(taskId),
    enabled: !!taskId,
    refetchInterval: POLLING_INTERVAL,
  });
}

export function useCreateTask() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: TaskCreate) => createTask(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      queryClient.invalidateQueries({ queryKey: ['metrics'] });
    },
  });
}

export function useCancelTask() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => cancelTask(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      queryClient.invalidateQueries({ queryKey: ['metrics'] });
    },
  });
}
