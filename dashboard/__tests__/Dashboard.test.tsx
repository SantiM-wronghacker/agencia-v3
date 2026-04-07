import React from 'react';
import { render, screen } from '@testing-library/react';

// Mock react-router-dom
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => jest.fn(),
  NavLink: ({ children, to }: { children: React.ReactNode; to: string }) => <a href={to}>{children}</a>,
}));

// Mock react-query
jest.mock('@tanstack/react-query', () => ({
  useQuery: () => ({ data: undefined, isLoading: true, error: null }),
  useMutation: () => ({ mutate: jest.fn() }),
  useQueryClient: () => ({ invalidateQueries: jest.fn() }),
}));

import Dashboard from '../src/pages/Dashboard';

test('renders dashboard page with loading state', () => {
  render(<Dashboard />);
  // Dashboard should render without crashing
  expect(document.querySelector('[class]')).toBeTruthy();
});
