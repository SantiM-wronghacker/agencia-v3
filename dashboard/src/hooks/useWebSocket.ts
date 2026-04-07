import { useState, useEffect, useCallback, useRef } from 'react';
import WebSocketService from '../services/websocketService';

export function useWebSocket() {
  const [lastMessage, setLastMessage] = useState<unknown>(null);
  const [isConnected, setIsConnected] = useState(false);
  const mountedRef = useRef(true);

  const handleMessage = useCallback((data: unknown) => {
    if (mountedRef.current) {
      setLastMessage(data);
    }
  }, []);

  useEffect(() => {
    mountedRef.current = true;
    const ws = WebSocketService.getInstance();
    const unsubMessage = ws.onMessage(handleMessage);
    const unsubConnect = ws.onConnect(() => {
      if (mountedRef.current) setIsConnected(true);
    });
    const unsubDisconnect = ws.onDisconnect(() => {
      if (mountedRef.current) setIsConnected(false);
    });

    ws.connect();
    setIsConnected(ws.isConnected);

    return () => {
      mountedRef.current = false;
      unsubMessage();
      unsubConnect();
      unsubDisconnect();
      // Don't disconnect the singleton - other components may be using it
    };
  }, [handleMessage]);

  return { lastMessage, isConnected };
}
