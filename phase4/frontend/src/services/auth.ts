import axios from 'axios';

interface User {
  id: string;
  email: string;
  role: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

interface UserCreate {
  email: string;
  password: string;
  confirm_password: string;
}

interface UserLogin {
  email: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

interface TokenRefresh {
  refresh_token: string;
}

class AuthService {
  private API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || this.detectApiBaseUrl();

  private detectApiBaseUrl(): string {
    // In browser environments, we might need to use the WSL IP
    if (typeof window !== 'undefined') {
      // Check if we're in a development environment
      const isDev = process.env.NODE_ENV === 'development';

      // For WSL development, try the known WSL IP first
      if (isDev) {
        return 'http://172.28.224.12:8000';
      }
    }

    // Default fallback
    return 'http://localhost:8000';
  }
  private TOKEN_KEY = 'todo_app_token';
  private REFRESH_TOKEN_KEY = 'todo_app_refresh_token';

  // Register a new user
  async register(email: string, password: string): Promise<User> {
    try {
      const userData: UserCreate = {
        email,
        password,
        confirm_password: password,
      };

      const response = await axios.post(`${this.API_BASE_URL}/auth/signup`, userData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // Login user
  async login(email: string, password: string): Promise<LoginResponse> {
    try {
      const loginData: UserLogin = {
        email,
        password,
      };

      const response = await axios.post(`${this.API_BASE_URL}/auth/login`, loginData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const { access_token, refresh_token } = response.data;
      this.setToken(access_token);
      this.setRefreshToken(refresh_token);

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // Refresh access token
  async refreshToken(): Promise<string> {
    try {
      const refreshToken = this.getRefreshToken();
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const refreshData: TokenRefresh = {
        refresh_token: refreshToken,
      };

      const response = await axios.post(`${this.API_BASE_URL}/auth/refresh`, refreshData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const { access_token } = response.data;
      this.setToken(access_token);

      return access_token;
    } catch (error) {
      // If refresh token fails, clear both tokens
      this.logout();
      throw this.handleError(error);
    }
  }

  // Get user profile
  async getUserProfile(): Promise<User> {
    try {
      const response = await axios.get(`${this.API_BASE_URL}/auth/me`, {
        headers: this.getAuthHeaders(),
      });

      return response.data;
    } catch (error) {
      // If getting profile fails, check if it's due to expired token
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        // Try to refresh token and retry
        try {
          await this.refreshToken();
          const response = await axios.get(`${this.API_BASE_URL}/auth/me`, {
            headers: this.getAuthHeaders(),
          });
          return response.data;
        } catch (refreshError) {
          throw this.handleError(refreshError);
        }
      }
      throw this.handleError(error);
    }
  }

  // Logout user
  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
  }

  // Get access token
  getToken(): string | null {
    const token = typeof window !== 'undefined' ? localStorage.getItem(this.TOKEN_KEY) : null;

    // Check if token is expired by decoding it
    if (token) {
      try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(
          atob(base64)
            .split('')
            .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
            .join('')
        );

        const decoded = JSON.parse(jsonPayload);
        const currentTime = Math.floor(Date.now() / 1000);

        if (decoded.exp < currentTime) {
          // Token is expired, remove it
          this.logout();
          return null;
        }
      } catch (error) {
        console.error('Error decoding token:', error);
        return null;
      }
    }

    return token;
  }

  // Get refresh token
  getRefreshToken(): string | null {
    return typeof window !== 'undefined' ? localStorage.getItem(this.REFRESH_TOKEN_KEY) : null;
  }

  // Set access token
  private setToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.TOKEN_KEY, token);
    }
  }

  // Set refresh token
  private setRefreshToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.REFRESH_TOKEN_KEY, token);
    }
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  // Get authenticated user info (from token)
  getCurrentUser(): { user_id: string; email: string } | null {
    const token = this.getToken();
    if (!token) return null;

    try {
      // Decode JWT token to get user info
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );

      const decoded = JSON.parse(jsonPayload);
      return {
        user_id: decoded.sub,
        email: decoded.email || decoded.username || decoded.name,
      };
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  }

  // Add auth headers to requests
  getAuthHeaders(): object {
    const token = this.getToken(); // This will handle expired tokens
    return {
      Authorization: token ? `Bearer ${token}` : '',
      'Content-Type': 'application/json',
    };
  }

  private handleError(error: any): Error {
    if (axios.isAxiosError(error)) {
      if (error.response) {
        // Server responded with error status
        const message = error.response.data?.detail || error.response.data?.message || 'An error occurred';
        return new Error(message);
      } else if (error.request) {
        // Request was made but no response received
        return new Error('Network error - could not reach server');
      } else {
        // Something else happened while setting up the request
        return new Error(error.message || 'An unexpected error occurred');
      }
    } else {
      // Non-Axios error
      return new Error(error.message || 'An unexpected error occurred');
    }
  }
}

export const authService = new AuthService();