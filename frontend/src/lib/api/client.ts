import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { mockData } from '@/lib/mocks/mockData';
import { useSnackbar } from 'notistack';

// Types matching backend API schemas
export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  success: boolean;
}

export interface ApiError {
  message: string;
  code?: string;
  details?: any;
}

export interface User {
  id: string;
  email: string;
  role: 'agent' | 'expert' | 'admin';
  name: string;
  createdAt: string;
}

export interface Villa {
  id: string;
  name: string;
  location: string;
  description: string;
  amenities: string[];
  pricePerNight: number;
  maxGuests: number;
}

export interface Answer {
  id: string;
  questionText: string;
  answerText: string;
  confidenceScore: number;
  citations: Citation[];
  createdAt: string;
  userId: string;
}

export interface Citation {
  id: string;
  sourceName: string;
  snippetText: string;
  relevanceScore: number;
  sourceId: string;
}

export interface ExpertCorrection {
  id: string;
  answerId: string;
  correctionText: string;
  submittedBy: User;
  status: 'pending' | 'approved' | 'rejected';
  createdAt: string;
}

export interface KnowledgeSource {
  id: string;
  name: string;
  type: 'faq' | 'review' | 'policy' | 'manual';
  sourceUrl?: string;
  indexedAt: string;
  documentCount: number;
}

export interface CoverageGap {
  id: string;
  questionText: string;
  topic: string;
  severity: 'low' | 'medium' | 'high';
  reportedBy: User;
  createdAt: string;
}

export interface AuditLog {
  id: string;
  userId: string;
  action: string;
  resourceType: string;
  resourceId: string;
  details: any;
  timestamp: string;
}

// Mock mode flag - set to true for development without backend
const USE_MOCK_DATA = process.env.NEXT_PUBLIC_USE_MOCK_DATA === 'true' || true;

class ApiClient {
  private client: AxiosInstance;
  private mockMode: boolean;

  constructor() {
    this.mockMode = USE_MOCK_DATA;
    
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for adding auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token');
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
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized - redirect to login
          localStorage.removeItem('auth_token');
          localStorage.removeItem('user_email');
          window.location.href = '/login';
        }
        
        const errorMessage = error.response?.data?.message || error.message || 'An error occurred';
        
        // Show snackbar notification
        if (typeof window !== 'undefined') {
          // Defer to component-level notification for better UX
          console.error('API Error:', errorMessage);
        }
        
        return Promise.reject(error);
      }
    );
  }

  // Mock data simulation helper
  private async simulateDelay(ms = 500): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Auth endpoints
  async login(email: string, password: string): Promise<ApiResponse<{ token: string; user: User }>> {
    if (this.mockMode) {
      await this.simulateDelay();
      const user = mockData.users.find(u => u.email === email);
      if (user && password === 'password') {
        return {
          data: {
            token: `mock_jwt_${Date.now()}`,
            user,
          },
          success: true,
          message: 'Login successful',
        };
      }
      throw new Error('Invalid credentials');
    }

    return this.client.post('/auth/login', { email, password });
  }

  async logout(): Promise<ApiResponse> {
    if (this.mockMode) {
      await this.simulateDelay();
      return {
        data: {},
        success: true,
        message: 'Logged out successfully',
      };
    }

    return this.client.post('/auth/logout');
  }

  async getProfile(): Promise<ApiResponse<User>> {
    if (this.mockMode) {
      await this.simulateDelay();
      const storedEmail = localStorage.getItem('user_email');
      const user = mockData.users.find(u => u.email === storedEmail) || mockData.users[0];
      return {
        data: user,
        success: true,
      };
    }

    return this.client.get('/auth/profile');
  }

  // Q&A endpoints
  async askQuestion(questionText: string): Promise<ApiResponse<Answer>> {
    if (this.mockMode) {
      await this.simulateDelay(800);
      
      // Generate a mock answer
      const mockAnswer: Answer = {
        id: `answer_${Date.now()}`,
        questionText,
        answerText: `Based on our knowledge base for villa rentals, ${questionText.toLowerCase().includes('cancellation') 
          ? 'the cancellation policy allows free cancellation up to 30 days before arrival. Please refer to the villa-specific policy document for details.' 
          : questionText.toLowerCase().includes('amenities') 
          ? 'VIP villas typically include private pools, ocean views, daily housekeeping, concierge service, and gourmet kitchen facilities.' 
          : 'Villa Serenity offers premium accommodations with stunning views and exceptional service tailored to luxury travelers.'}`,
        confidenceScore: Math.random() > 0.3 ? 0.85 : Math.random() > 0.5 ? 0.65 : 0.45,
        citations: mockData.citations.slice(0, Math.floor(Math.random() * 3) + 1),
        createdAt: new Date().toISOString(),
        userId: 'user_1',
      };

      return {
        data: mockAnswer,
        success: true,
        message: 'Answer generated successfully',
      };
    }

    return this.client.post('/answers/ask', { questionText });
  }

  async getAnswers(limit = 20, offset = 0): Promise<ApiResponse<Answer[]>> {
    if (this.mockMode) {
      await this.simulateDelay();
      return {
        data: mockData.answers.slice(offset, offset + limit),
        success: true,
      };
    }

    return this.client.get('/answers', { params: { limit, offset } });
  }

  async getAnswerById(id: string): Promise<ApiResponse<Answer>> {
    if (this.mockMode) {
      await this.simulateDelay();
      const answer = mockData.answers.find(a => a.id === id) || mockData.answers[0];
      return {
        data: answer,
        success: true,
      };
    }

    return this.client.get(`/answers/${id}`);
  }

  // Admin endpoints
  async getUsers(): Promise<ApiResponse<User[]>> {
    if (this.mockMode) {
      await this.simulateDelay();
      return {
        data: mockData.users,
        success: true,
      };
    }

    return this.client.get('/admin/users');
  }

  async updateUser(id: string, updates: Partial<User>): Promise<ApiResponse<User>> {
    if (this.mockMode) {
      await this.simulateDelay();
      const userIndex = mockData.users.findIndex(u => u.id === id);
      if (userIndex >= 0) {
        mockData.users[userIndex] = { ...mockData.users[userIndex], ...updates };
        return {
          data: mockData.users[userIndex],
          success: true,
          message: 'User updated successfully',
        };
      }
      throw new Error('User not found');
    }

    return this.client.put(`/admin/users/${id}`, updates);
  }

  async getCorrections(): Promise<ApiResponse<ExpertCorrection[]>> {
    if (this.mockMode) {
      await this.simulateDelay();
      return {
        data: mockData.corrections,
        success: true,
      };
    }

    return this.client.get('/corrections');
  }

  async approveCorrection(id: string): Promise<ApiResponse<ExpertCorrection>> {
    if (this.mockMode) {
      await this.simulateDelay();
      const correction = mockData.corrections.find(c => c.id === id);
      if (correction) {
        correction.status = 'approved';
        return {
          data: correction,
          success: true,
          message: 'Correction approved',
        };
      }
      throw new Error('Correction not found');
    }

    return this.client.patch(`/corrections/${id}/approve`);
  }

  async getAuditLogs(): Promise<ApiResponse<AuditLog[]>> {
    if (this.mockMode) {
      await this.simulateDelay();
      return {
        data: mockData.auditLogs,
        success: true,
      };
    }

    return this.client.get('/admin/audit');
  }

  async getKnowledgeSources(): Promise<ApiResponse<KnowledgeSource[]>> {
    if (this.mockMode) {
      await this.simulateDelay();
      return {
        data: mockData.knowledgeSources,
        success: true,
      };
    }

    return this.client.get('/knowledge-sources');
  }

  async getCoverageGaps(): Promise<ApiResponse<CoverageGap[]>> {
    if (this.mockMode) {
      await this.simulateDelay();
      return {
        data: mockData.coverageGaps,
        success: true,
      };
    }

    return this.client.get('/coverage-gaps');
  }
}

export const api = new ApiClient();
export default api;