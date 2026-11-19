'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI } from '@/lib/api/client';

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'agent' | 'expert' | 'admin';
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  isAuthenticated: boolean;
  hasRole: (role: User['role'] | User['role'][]) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Initialize auth state from localStorage
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const token = localStorage.getItem('auth_token');
        if (token) {
          // Try to get user profile
          const response = await authAPI.getProfile();
          if (response.status === 200) {
            setUser(response.data.user);
          } else {
            // Token might be invalid, clear it
            localStorage.removeItem('auth_token');
            localStorage.removeItem('user_role');
          }
        }
      } catch (err) {
        console.error('Failed to initialize auth:', err);
        // Clear invalid tokens
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_role');
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await authAPI.login(email, password);
      
      if (response.status === 200 && response.data.token) {
        const { token, user } = response.data;
        
        // Store token and user info
        localStorage.setItem('auth_token', token);
        localStorage.setItem('user_role', user.role);
        setUser(user);
        
        // Redirect to dashboard
        window.location.href = '/dashboard';
      } else {
        throw new Error('Invalid login response');
      }
    } catch (err: any) {
      setError(err.message || 'Login failed. Please check your credentials.');
      setLoading(false);
      throw err;
    }
  };

  const logout = () => {
    // Clear auth data
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_role');
    setUser(null);
    
    // Redirect to login
    window.location.href = '/login';
  };

  const refreshUser = async () => {
    if (!user) return;
    
    try {
      const response = await authAPI.getProfile();
      if (response.status === 200) {
        setUser(response.data.user);
      }
    } catch (err) {
      console.error('Failed to refresh user:', err);
    }
  };

  const hasRole = (role: User['role'] | User['role'][]) => {
    if (!user) return false;
    
    if (Array.isArray(role)) {
      return role.includes(user.role);
    }
    
    return user.role === role;
  };

  const value: AuthContextType = {
    user,
    loading,
    error,
    login,
    logout,
    refreshUser,
    isAuthenticated: !!user,
    hasRole,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthProvider;