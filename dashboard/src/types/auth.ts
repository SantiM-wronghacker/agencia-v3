export type UserRole = 'admin' | 'user' | 'viewer';

export interface AuthUser {
  sub: string;
  role: UserRole;
  exp: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}
