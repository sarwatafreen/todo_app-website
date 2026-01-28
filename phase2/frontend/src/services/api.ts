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
      const response: AxiosResponse<Todo[]> = await axios.get(
        `${this.API_BASE_URL}/api/${userId}/tasks`,
        { headers: authService.getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
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
      throw this.handleError(error);
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
      throw this.handleError(error);
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
      throw this.handleError(error);
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
      throw this.handleError(error);
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
      throw this.handleError(error);
    }
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
      return new Error(error instanceof Error ? error.message : 'An unexpected error occurred');
    }
  }
}

export const todoApiService = new TodoApiService();