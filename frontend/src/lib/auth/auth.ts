import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { jwtDecode, JwtPayload } from 'jwt-decode';

interface User {
  id: string;
  email: string;
  role: 'agent' | 'expert' | 'admin';
  name: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  hasRole: (role: User['role']) => boolean;
  isAuthenticated: boolean;
}

// Mock user data for development
const MOCK_USERS: User[] = [
  { id: '1', email: 'agent@example.com', role: 'agent', name: 'John Agent' },
  { id: '2', email: 'expert@example.com', role: 'expert', name: 'Sarah Expert' },
  { id: '3', email: 'admin@example.com', role: 'admin', name: 'Admin User' },
];

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for stored token on mount
    const storedToken = localStorage.getItem('auth_token');
    if (storedToken) {
      try {
        // In production, this would decode the JWT
        // const decoded = jwtDecode<JwtPayload & { role: string; email: string; id: string }>(storedToken);
        
        // For mock purposes, find user by email from token
        const mockEmail = localStorage.getItem('user_email') || 'agent@example.com';
        const foundUser = MOCK_USERS.find(u => u.email === mockEmail) || MOCK_USERS[0];
        
        setToken(storedToken);
        setUser(foundUser);
      } catch (error) {
        console.error('Failed to decode token:', error);
        localStorage.removeItem('auth_token');
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Find user (mock authentication)
      const foundUser = MOCK_USERS.find(u => u.email === email);
      if (!foundUser) {
        throw new Error('Invalid credentials');
      }
      
      // Generate mock token
      const mockToken = `mock_jwt_${Date.now()}`;
      
      // Store token and user
      localStorage.setItem('auth_token', mockToken);
      localStorage.setItem('user_email', email);
      
      setToken(mockToken);
      setUser(foundUser);
    } catch (error) {
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_email');
    setToken(null);
    setUser(null);
  };

  const hasRole = (role: User['role']) => {
    return user?.role === role;
  };

  const value: AuthContextType = {
    user,
    token,
    isLoading,
    login,
    logout,
    hasRole,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
