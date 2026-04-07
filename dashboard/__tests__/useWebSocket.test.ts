import WebSocketService from '../src/services/websocketService';

describe('WebSocketService', () => {
  test('is a singleton', () => {
    const instance1 = WebSocketService.getInstance();
    const instance2 = WebSocketService.getInstance();
    expect(instance1).toBe(instance2);
  });
});
