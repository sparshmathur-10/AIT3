import axios, { AxiosInstance } from 'axios';
import { User, Todo, AuthResponse, AIPlanningResponse, CreateTodoRequest } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://aitodo-backend.onrender.com/api';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include auth token
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle token refresh
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
              const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
                refresh: refreshToken,
              });
              const { access } = response.data;
              localStorage.setItem('access_token', access);
              originalRequest.headers.Authorization = `Bearer ${access}`;
              return this.api(originalRequest);
            }
          } catch (refreshError) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication
  async googleAuth(token: string): Promise<AuthResponse> {
    const response = await this.api.post('/auth/google/', { token });
    return response.data;
  }

  // Todos
  async getTodos(): Promise<Todo[]> {
    const response = await this.api.get('/todos/');
    return response.data;
  }

  async createTodo(todo: CreateTodoRequest): Promise<Todo> {
    const response = await this.api.post('/todos/', todo);
    return response.data;
  }

  async updateTodo(id: number, todo: Partial<Todo>): Promise<Todo> {
    const response = await this.api.patch(`/todos/${id}/`, todo);
    return response.data;
  }

  async deleteTodo(id: number): Promise<void> {
    await this.api.delete(`/todos/${id}/`);
  }

  // AI Planning
  async planWithAI(tasks: string[]): Promise<AIPlanningResponse> {
    const response = await this.api.post('/todos/plan/', { tasks });
    return response.data;
  }
}

export const apiService = new ApiService(); 