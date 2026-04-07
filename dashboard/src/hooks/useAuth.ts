import { useState, useCallback } from 'react';
import { AuthUser } from '../types/auth';

export function useAuth() {
  const [token, setToken] = useState<string | null>(
    () => localStorage.getItem('auth_token')
  );
  const [user, setUser] = useState<AuthUser | null>(() => {
    const stored = localStorage.getItem('auth_user');
    return stored ? JSON.parse(stored) : null;
  });

  const isAuthenticated = !!token;

  // NOTE: This is a mock login. Replace with a real API call in production.
  const login = useCallback(async (username: string, _password: string) => {
    const mockToken = 'placeholder-jwt-token';
    const mockUser: AuthUser = {
      sub: username,
      role: 'admin',
      exp: new Date(Date.now() + 86400000).toISOString(),
    };
    localStorage.setItem('auth_token', mockToken);
    localStorage.setItem('auth_user', JSON.stringify(mockUser));
    setToken(mockToken);
    setUser(mockUser);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    setToken(null);
    setUser(null);
  }, []);

  return { token, user, isAuthenticated, login, logout };
}
