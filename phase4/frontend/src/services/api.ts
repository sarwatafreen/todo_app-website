import axios, { AxiosResponse } from 'axios';
import { authService } from './auth';

interface Todo {
  id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  owner_id: string;
  created_at: string;
  updated_at: string;
  due_date?: string;
}

interface TodoCreate {
  title: string;
  description?: string;
  due_date?: string;
}

interface TodoUpdate {
  title?: string;
  description?: string;
  is_completed?: boolean;
  due_date?: string;
}

class TodoApiService {
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

  // Get all todos for a user
  async getUserTodos(userId: string): Promise<Todo[]> {
    try {
      // Verify we have a valid user ID
      if (!userId) {
        throw new Error('User ID is required to fetch tasks');
      }

      // Verify we have valid authentication
      const authHeaders = authService.getAuthHeaders() as Record<string, string>;
      if (!authHeaders || !authHeaders['Authorization'] || authHeaders['Authorization'] === 'Bearer ') {
        throw new Error('Authentication required. Please log in first.');
      }

      console.log(`Fetching todos for user: ${userId} from ${this.API_BASE_URL}/api/${userId}/tasks`);

      const response: AxiosResponse<Todo[]> = await axios.get(
        `${this.API_BASE_URL}/api/${userId}/tasks`,
        {
          headers: authHeaders,
          timeout: 30000 // 30 second timeout
        }
      );

      console.log(`Successfully fetched ${response.data.length} todos`);
      return response.data;
    } catch (error) {
      console.error('Error fetching user todos:', error);

      // Check if it's a network error and try alternative endpoints
      if (axios.isAxiosError(error) && !error.response && error.request) {
        console.log('Network error detected, attempting fallback URL...');

        // Try the WSL IP as a fallback
        const fallbackUrl = 'http://172.28.224.12:8000';
        if (this.API_BASE_URL !== fallbackUrl) {
          console.log(`Trying fallback URL: ${fallbackUrl}/api/${userId}/tasks`);

          try {
            const fallbackResponse: AxiosResponse<Todo[]> = await axios.get(
              `${fallbackUrl}/api/${userId}/tasks`,
              {
                headers: authService.getAuthHeaders(),
                timeout: 30000
              }
            );

            console.log(`Successfully fetched ${fallbackResponse.data.length} todos from fallback URL`);
            return fallbackResponse.data;
          } catch (fallbackError) {
            console.error('Fallback request also failed:', fallbackError);
          }
        }
      }

      const handledError = await this.handleError(error);

      // If token was refreshed, try the request again once
      if (handledError.message === 'TOKEN_REFRESHED_RETRIES_NEEDED') {
        console.log('Retrying request after token refresh...');

        // Get new headers with refreshed token
        const newAuthHeaders = authService.getAuthHeaders() as Record<string, string>;
        if (!newAuthHeaders || !newAuthHeaders['Authorization'] || newAuthHeaders['Authorization'] === 'Bearer ') {
          throw new Error('Authentication required. Please log in first.');
        }

        const response: AxiosResponse<Todo[]> = await axios.get(
          `${this.API_BASE_URL}/api/${userId}/tasks`,
          {
            headers: newAuthHeaders,
            timeout: 30000 // 30 second timeout
          }
        );

        console.log(`Successfully fetched ${response.data.length} todos after retry`);
        return response.data;
      }

      throw handledError;
    }
  }

  // Create a new todo
  async createTodo(userId: string, todoData: TodoCreate): Promise<Todo> {
    // Format the request payload properly
    const payload: any = {
      ...todoData
    };

    // Handle date formatting if due_date is provided
    if (todoData.due_date) {
      // If it's already a Date object, convert to ISO string
      if ((todoData.due_date as any) instanceof Date) {
        payload.due_date = ((todoData.due_date as any) as Date).toISOString();
      }
      // If it's a string in YYYY-MM-DD format, convert to ISO string
      else if (typeof todoData.due_date === 'string' && todoData.due_date.match(/^\d{4}-\d{2}-\d{2}$/)) {
        payload.due_date = new Date(todoData.due_date).toISOString();
      }
      // Otherwise, leave it as is (might already be ISO string)
      else {
        payload.due_date = todoData.due_date as string;
      }
    }

    // Remove undefined values to avoid sending them to the backend
    Object.keys(payload).forEach(key => {
      if (payload[key] === undefined) {
        delete payload[key];
      }
    });

    try {
      const response: AxiosResponse<Todo> = await axios.post(
        `${this.API_BASE_URL}/api/${userId}/tasks`,
        payload,
        { headers: authService.getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      // Check if it's a network error and try alternative endpoints
      if (axios.isAxiosError(error) && !error.response && error.request) {
        console.log('Network error detected during create, attempting fallback URL...');

        // Try the WSL IP as a fallback
        const fallbackUrl = 'http://172.28.224.12:8000';
        if (this.API_BASE_URL !== fallbackUrl) {
          console.log(`Trying fallback URL for create: ${fallbackUrl}/api/${userId}/tasks`);

          try {
            const fallbackResponse: AxiosResponse<Todo> = await axios.post(
              `${fallbackUrl}/api/${userId}/tasks`,
              payload,
              { headers: authService.getAuthHeaders() }
            );

            console.log('Successfully created todo with fallback URL');
            return fallbackResponse.data;
          } catch (fallbackError) {
            console.error('Fallback create request also failed:', fallbackError);
          }
        }
      }

      const handledError = await this.handleError(error);

      // If token was refreshed, try the request again once
      if (handledError.message === 'TOKEN_REFRESHED_RETRIES_NEEDED') {
        console.log('Retrying create todo after token refresh...');

        const response: AxiosResponse<Todo> = await axios.post(
          `${this.API_BASE_URL}/api/${userId}/tasks`,
          payload,
          { headers: authService.getAuthHeaders() }
        );
        return response.data;
      }

      throw handledError;
    }
  }

  // Get a specific todo
  async getTodoById(userId: string, todoId: string): Promise<Todo> {
    try {
      const response: AxiosResponse<Todo> = await axios.get(
        `${this.API_BASE_URL}/api/${userId}/tasks/${todoId}`,
        { headers: authService.getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      const handledError = await this.handleError(error);

      // If token was refreshed, try the request again once
      if (handledError.message === 'TOKEN_REFRESHED_RETRIES_NEEDED') {
        console.log('Retrying get todo by ID after token refresh...');

        const response: AxiosResponse<Todo> = await axios.get(
          `${this.API_BASE_URL}/api/${userId}/tasks/${todoId}`,
          { headers: authService.getAuthHeaders() }
        );
        return response.data;
      }

      throw handledError;
    }
  }

  // Update a todo
  async updateTodo(userId: string, todoId: string, todoData: TodoUpdate): Promise<Todo> {
    try {
      // Format the request payload properly
      const payload: any = {
        ...todoData
      };

      // Handle date formatting if due_date is provided
      if (todoData.due_date) {
        // If it's already a Date object, convert to ISO string
        if ((todoData.due_date as any) instanceof Date) {
          payload.due_date = ((todoData.due_date as any) as Date).toISOString();
        }
        // If it's a string in YYYY-MM-DD format, convert to ISO string
        else if (typeof todoData.due_date === 'string' && (todoData.due_date as string).match(/^\d{4}-\d{2}-\d{2}$/)) {
          payload.due_date = new Date(todoData.due_date as string).toISOString();
        }
        // Otherwise, leave it as is (might already be ISO string)
        else {
          payload.due_date = todoData.due_date as string;
        }
      }

      // Remove undefined values to avoid sending them to the backend
      Object.keys(payload).forEach(key => {
        if (payload[key] === undefined) {
          delete payload[key];
        }
      });

      const response: AxiosResponse<Todo> = await axios.put(
        `${this.API_BASE_URL}/api/${userId}/tasks/${todoId}`,
        payload,
        { headers: authService.getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      const handledError = await this.handleError(error);

      // If token was refreshed, try the request again once
      if (handledError.message === 'TOKEN_REFRESHED_RETRIES_NEEDED') {
        console.log('Retrying update todo after token refresh...');

        const payload: any = {
          ...todoData
        };

        // Handle date formatting if due_date is provided
        if (todoData.due_date) {
          // If it's already a Date object, convert to ISO string
          if ((todoData.due_date as any) instanceof Date) {
            payload.due_date = ((todoData.due_date as unknown) as Date).toISOString();
          }
          // If it's a string in YYYY-MM-DD format, convert to ISO string
          else if (typeof todoData.due_date === 'string' && todoData.due_date.match(/^\d{4}-\d{2}-\d{2}$/)) {
            payload.due_date = new Date(todoData.due_date).toISOString();
          }
          // Otherwise, leave it as is (might already be ISO string)
          else {
            payload.due_date = todoData.due_date;
          }
        }

        // Remove undefined values to avoid sending them to the backend
        Object.keys(payload).forEach(key => {
          if (payload[key] === undefined) {
            delete payload[key];
          }
        });

        const response: AxiosResponse<Todo> = await axios.put(
          `${this.API_BASE_URL}/api/${userId}/tasks/${todoId}`,
          payload,
          { headers: authService.getAuthHeaders() }
        );
        return response.data;
      }

      throw handledError;
    }
  }

  // Delete a todo
  async deleteTodo(userId: string, todoId: string): Promise<void> {
    try {
      await axios.delete(
        `${this.API_BASE_URL}/api/${userId}/tasks/${todoId}`,
        { headers: authService.getAuthHeaders() }
      );
    } catch (error) {
      const handledError = await this.handleError(error);

      // If token was refreshed, try the request again once
      if (handledError.message === 'TOKEN_REFRESHED_RETRIES_NEEDED') {
        console.log('Retrying delete todo after token refresh...');

        await axios.delete(
          `${this.API_BASE_URL}/api/${userId}/tasks/${todoId}`,
          { headers: authService.getAuthHeaders() }
        );
        return;
      }

      throw handledError;
    }
  }

  // Toggle todo completion status
  async toggleTodoCompletion(userId: string, todoId: string, isCompleted: boolean): Promise<Todo> {
    try {
      const response: AxiosResponse<Todo> = await axios.patch(
        `${this.API_BASE_URL}/api/${userId}/tasks/${todoId}/complete`,
        { is_completed: isCompleted },
        { headers: authService.getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      const handledError = await this.handleError(error);

      // If token was refreshed, try the request again once
      if (handledError.message === 'TOKEN_REFRESHED_RETRIES_NEEDED') {
        console.log('Retrying toggle todo completion after token refresh...');

        const response: AxiosResponse<Todo> = await axios.patch(
          `${this.API_BASE_URL}/api/${userId}/tasks/${todoId}/complete`,
          { is_completed: isCompleted },
          { headers: authService.getAuthHeaders() }
        );
        return response.data;
      }

      throw handledError;
    }
  }

  private async handleError(error: any): Promise<Error> {
    console.error('API service error:', error);

    if (axios.isAxiosError(error)) {
      if (error.response) {
        // Check if it's an authentication error (401)
        if (error.response.status === 401) {
          console.error('Authentication error - token may be expired');

          // Try to refresh the token
          try {
            await authService.refreshToken();

            // Return a special error to indicate token was refreshed and request should be retried
            return new Error('TOKEN_REFRESHED_RETRIES_NEEDED');
          } catch (refreshError) {
            console.error('Failed to refresh token:', refreshError);
            // If refresh fails, clear tokens and return authentication error
            authService.logout();
            return new Error('Authentication failed. Please log in again.');
          }
        }

        // Server responded with error status
        console.error('Server error:', error.response.status, error.response.data);

        // Handle validation errors specifically (HTTP 422)
        if (error.response.status === 422) {
          console.error('Validation error details:', error.response.data);

          // Extract detailed validation error information from Pydantic
          if (error.response.data && typeof error.response.data === 'object' && error.response.data.detail) {
            if (Array.isArray(error.response.data.detail)) {
              // Format Pydantic validation error array
              const validationErrors = error.response.data.detail;
              const errorMessages = validationErrors.map((err: any) => {
                const field = Array.isArray(err.loc) ? err.loc.slice(-1)[0] : 'unknown'; // Get the last element of loc array (the actual field name)
                return `${field}: ${err.msg}`;
              });
              return new Error(`Validation Error: ${errorMessages.join(', ')}`);
            } else {
              // Single detail message
              return new Error(`Validation Error: ${error.response.data.detail}`);
            }
          }
          return new Error('Validation Error: Invalid data provided');
        }

        const message = error.response.data?.detail || error.response.data?.message || `Server error: ${error.response.status}`;
        return new Error(message);
      } else if (error.request) {
        // Request was made but no response received
        console.error('Network error:', error.request);

        // Check if we're in a WSL environment and the server might be unreachable
        if (typeof window !== 'undefined') {
          // Provide more specific guidance for WSL users
          return new Error('Network error - could not reach server. If using WSL, make sure the backend server is running and the API URL is correctly configured. Please check your connection and try again.');
        }

        return new Error('Network error - could not reach server. Please check your connection and try again.');
      } else {
        // Something else happened while setting up the request
        console.error('Request setup error:', error.message);
        return new Error(error.message || 'An unexpected error occurred while setting up the request');
      }
    } else {
      // Non-Axios error
      return new Error(error instanceof Error ? error.message : 'An unexpected error occurred');
    }
  }
}

export const todoApiService = new TodoApiService();




