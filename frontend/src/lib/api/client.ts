import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { mockData } from '@/lib/mocks/mockData';

export interface ApiError {
  status: number;
  message: string;
  details?: Record<string, any>;
}

export interface ApiResponse<T = any> {
  data: T;
  status: number;
  statusText: string;
}

class ApiClient {
  private client: AxiosInstance;
  private useMockFallback = process.env.NEXT_PUBLIC_USE_MOCK_DATA === 'true' || process.env.NODE_ENV === 'development';

  constructor() {
    // Base API URL - fallback to mock if not configured
    const baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';
    
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for adding auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getAuthToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Handle unauthorized access
          this.handleUnauthorized();
        }
        return Promise.reject(this.normalizeError(error));
      }
    );
  }

  private getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');
    }
    return null;
  }

  private handleUnauthorized(): void {
    // Clear auth data and redirect to login
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
      sessionStorage.removeItem('auth_token');
      localStorage.removeItem('user_role');
      window.location.href = '/login';
    }
  }

  private normalizeError(error: AxiosError): ApiError {
    const status = error.response?.status || 500;
    let message = error.message || 'An unexpected error occurred';

    if (error.response?.data && typeof error.response.data === 'object') {
      const errorData = error.response.data as any;
      message = errorData.message || errorData.detail || message;
    }

    return {
      status,
      message,
      details: error.response?.data as Record<string, any>,
    };
  }

  private async mockRequest<T>(endpoint: string, options?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    console.log(`Using mock data for: ${endpoint}`);
    
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 200));

    // Mock endpoint mappings
    const mockMap: Record<string, () => any> = {
      '/auth/login': () => ({
        token: 'mock-jwt-token',
        user: mockData.users.find(u => u.role === 'agent'),
      }),
      '/auth/profile': () => ({
        user: mockData.users.find(u => u.role === 'agent'),
      }),
      '/users': () => mockData.users,
      '/answers': () => mockData.answers,
      '/answers/ask': () => ({
        id: 'mock-answer-id',
        question: options?.data?.question || 'Sample question',
        answer: 'This is a mock answer from the knowledge assistant.',
        confidence: 0.85,
        citations: mockData.citations.slice(0, 3),
        created_at: new Date().toISOString(),
      }),
      '/villas': () => mockData.villas,
      '/knowledge-sources': () => mockData.knowledgeSources,
      '/corrections': () => mockData.expertCorrections,
      '/coverage-gaps': () => mockData.coverageGaps,
      '/admin/audit-logs': () => mockData.auditLogs,
    };

    const mockHandler = mockMap[endpoint];
    if (mockHandler) {
      return {
        data: mockHandler() as T,
        status: 200,
        statusText: 'OK',
      };
    }

    // Default fallback for unmapped endpoints
    return {
      data: { message: 'Mock response for endpoint not yet implemented' } as T,
      status: 200,
      statusText: 'OK',
    };
  }

  async request<T = any>(config: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      if (this.useMockFallback) {
        const endpoint = config.url || '';
        return this.mockRequest<T>(endpoint, config);
      }

      const response: AxiosResponse<T> = await this.client.request(config);
      return {
        data: response.data,
        status: response.status,
        statusText: response.statusText,
      };
    } catch (error) {
      if (this.useMockFallback) {
        // Fall back to mock data if real API fails
        const endpoint = config.url || '';
        return this.mockRequest<T>(endpoint, config);
      }
      throw error;
    }
  }

  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ ...config, method: 'GET', url });
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ ...config, method: 'POST', url, data });
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ ...config, method: 'PUT', url, data });
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ ...config, method: 'DELETE', url });
  }

  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ ...config, method: 'PATCH', url, data });
  }
}

// Create singleton instance
export const apiClient = new ApiClient();

// Helper functions for common API endpoints
export const authAPI = {
  login: (email: string, password: string) => 
    apiClient.post('/auth/login', { email, password }),
  logout: () => apiClient.post('/auth/logout'),
  getProfile: () => apiClient.get('/auth/profile'),
};

export const qaAPI = {
  askQuestion: (question: string) => 
    apiClient.post('/answers/ask', { question }),
  getAnswers: (page = 1, limit = 20) => 
    apiClient.get(`/answers?page=${page}&limit=${limit}`),
  getAnswer: (id: string) => 
    apiClient.get(`/answers/${id}`),
  submitCorrection: (answerId: string, correction: any) =>
    apiClient.post(`/answers/${id}/correct`, correction),
};

export const villaAPI = {
  getVillas: () => apiClient.get('/villas'),
  getVilla: (id: string) => apiClient.get(`/villas/${id}`),
};

export const adminAPI = {
  getUsers: () => apiClient.get('/users'),
  updateUser: (id: string, data: any) => apiClient.put(`/users/${id}`, data),
  getAuditLogs: () => apiClient.get('/admin/audit-logs'),
  getCoverageGaps: () => apiClient.get('/coverage-gaps'),
  getKnowledgeSources: () => apiClient.get('/knowledge-sources'),
};

export default apiClient;