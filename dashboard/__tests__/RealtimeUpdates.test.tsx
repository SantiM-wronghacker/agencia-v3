import React from 'react';
import { render, screen, act } from '@testing-library/react';

// Capture the last message handler registered by useWebSocket so we can
// simulate incoming messages from tests.
let triggerMessage: ((data: unknown) => void) | null = null;

jest.mock('../src/hooks/useWebSocket', () => ({
  useWebSocket: () => {
    const [lastMessage, setLastMessage] = React.useState<unknown>(null);
    // Expose the setter so the test can push messages.
    triggerMessage = (data: unknown) => setLastMessage(data);
    return { lastMessage, isConnected: true };
  },
}));

import RealtimeUpdates from '../src/components/RealtimeUpdates';

test('renders a received WS event using unified contract', () => {
  render(<RealtimeUpdates />);

  // Initially no events
  expect(screen.getByText(/No events yet/i)).toBeTruthy();

  // Simulate a message arriving with the unified contract { event, ts, payload }
  act(() => {
    triggerMessage?.({
      event: 'task_created',
      ts: '2026-03-05T23:00:00Z',
      payload: { id: '1', name: 'Test task' },
    });
  });

  // The event type should now be rendered
  expect(screen.getByText('task_created')).toBeTruthy();
});
