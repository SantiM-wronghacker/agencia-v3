import React from 'react';
import { render, screen } from '@testing-library/react';
import TaskCard from '../src/components/TaskCard';

const mockTask = {
  id: '1',
  name: 'Test Task',
  status: 'pending' as const,
  description: 'A test task',
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
  logs: [],
};

test('renders task name', () => {
  render(<TaskCard task={mockTask} />);
  expect(screen.getByText('Test Task')).toBeTruthy();
});

test('renders status badge', () => {
  render(<TaskCard task={mockTask} />);
  expect(screen.getByText('pending')).toBeTruthy();
});

test('renders cancel button for pending task', () => {
  render(<TaskCard task={mockTask} />);
  expect(screen.getByText('Cancel')).toBeTruthy();
});

test('does not render cancel button for completed task', () => {
  const completedTask = { ...mockTask, status: 'completed' as const };
  render(<TaskCard task={completedTask} />);
  expect(screen.queryByText('Cancel')).toBeNull();
});
