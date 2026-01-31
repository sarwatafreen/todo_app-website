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
  private API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

  // Get all todos for a user
  async getUserTodos(userId: string): Promise<Todo[]> {
    try {
      // Verify we have a valid user ID
      if (!userId) {
        throw new Error('User ID is required to fetch tasks');
      }

      // Verify we have valid authentication
      const authHeaders = authService.getAuthHeaders();
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

      const handledError = await this.handleError(error);

      // If token was refreshed, try the request again once
      if (handledError.message === 'TOKEN_REFRESHED_RETRIES_NEEDED') {
        console.log('Retrying request after token refresh...');

        // Get new headers with refreshed token
        const newAuthHeaders = authService.getAuthHeaders();
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
    try {
      const response: AxiosResponse<Todo> = await axios.post(
        `${this.API_BASE_URL}/api/${userId}/tasks`,
        todoData,
        { headers: authService.getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      const handledError = await this.handleError(error);

      // If token was refreshed, try the request again once
      if (handledError.message === 'TOKEN_REFRESHED_RETRIES_NEEDED') {
        console.log('Retrying create todo after token refresh...');

        const response: AxiosResponse<Todo> = await axios.post(
          `${this.API_BASE_URL}/api/${userId}/tasks`,
          todoData,
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
      const response: AxiosResponse<Todo> = await axios.put(
        `${this.API_BASE_URL}/api/${userId}/tasks/${todoId}`,
        todoData,
        { headers: authService.getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      const handledError = await this.handleError(error);

      // If token was refreshed, try the request again once
      if (handledError.message === 'TOKEN_REFRESHED_RETRIES_NEEDED') {
        console.log('Retrying update todo after token refresh...');

        const response: AxiosResponse<Todo> = await axios.put(
          `${this.API_BASE_URL}/api/${userId}/tasks/${todoId}`,
          todoData,
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
        const message = error.response.data?.detail || error.response.data?.message || `Server error: ${error.response.status}`;
        return new Error(message);
      } else if (error.request) {
        // Request was made but no response received
        console.error('Network error:', error.request);
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