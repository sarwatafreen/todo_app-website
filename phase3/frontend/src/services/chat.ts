import axios, { AxiosResponse } from 'axios';
import { authService } from './auth';

interface ChatRequest {
  message: string;
  conversation_id?: string;
}

interface ChatResponse {
  response: string;
  conversation_id: string;
  timestamp: string;
}

class ChatService {
  private API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

  async sendMessage(userId: string, message: string, conversationId?: string): Promise<ChatResponse> {
    try {
      // Verify we have a valid user ID
      if (!userId) {
        throw new Error('User ID is required to send a message');
      }

      // Verify we have a valid message
      if (!message || message.trim().length === 0) {
        throw new Error('Message cannot be empty');
      }

      // Verify we have valid authentication
      const authHeaders = authService.getAuthHeaders() as Record<string, string> | null;
      if (!authHeaders || !authHeaders['Authorization'] || authHeaders['Authorization'] === 'Bearer ') {
        throw new Error('Authentication required. Please log in first.');
      }

      const requestData: ChatRequest = {
        message: message.trim(),
        conversation_id: conversationId
      };

      const response: AxiosResponse<ChatResponse> = await axios.post(
        `${this.API_BASE_URL}/api/${userId}/chat`,
        requestData,
        {
          headers: authHeaders,
          timeout: 30000 // 30 second timeout
        }
      );

      return response.data;
    } catch (error) {
      console.error('Chat service error:', error);

      if (axios.isAxiosError(error)) {
        if (error.response) {
          // Server responded with error status
          console.error('Server error:', error.response.status, error.response.data);
          const message = error.response.data?.detail || error.response.data?.message || `Server error: ${error.response.status}`;
          throw new Error(message);
        } else if (error.request) {
          // Request was made but no response received
          console.error('Network error:', error.request);
          throw new Error('Network error - could not reach server. Please check your connection and try again.');
        } else {
          // Something else happened while setting up the request
          console.error('Request setup error:', error.message);
          throw new Error(error.message || 'An unexpected error occurred while setting up the request');
        }
      } else {
        // Non-Axios error
        throw new Error(error instanceof Error ? error.message : 'An unexpected error occurred');
      }
    }
  }
}

export const chatService = new ChatService();