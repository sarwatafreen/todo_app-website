'use client';

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/context/auth-context';
import { authService } from '@/services/auth';

export default function ChatInterface() {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Array<{
    role: 'user' | 'assistant';
    content: string;
    id: string;
  }>>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (chatContainerRef.current && messages.length > 0) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  // Auto-resize textarea
  useEffect(() => {
    const textarea = document.getElementById('prompt') as HTMLTextAreaElement;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 180) + 'px';
    }
  }, [inputValue]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading || !user?.user_id) return;

    const userMessage = {
      role: 'user' as const,
      content: inputValue,
      id: Date.now().toString(),
    };

    // Add user message to UI immediately
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputValue('');
    setIsLoading(true);

    try {
      // Use the user context for user ID and authService for the token
      const token = authService.getToken();

      if (!user?.user_id) {
        throw new Error('User not authenticated. Please log in first.');
      }

      const userId = user.user_id;

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`http://localhost:8000/api/${userId}/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: inputValue,
          conversation_id: conversationId || undefined,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to send message');
      }

      const data = await response.json();

      // Update conversation ID if this is the first message
      if (!conversationId) {
        setConversationId(data.conversation_id);
      }

      // Add AI response to messages
      const aiMessage = {
        role: 'assistant' as const,
        content: data.response,
        id: `ai-${Date.now()}`,
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: 'assistant' as const,
        content: 'Sorry, I encountered an issue processing your request. Please try again.',
        id: `error-${Date.now()}`,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (inputValue.trim() && !isLoading) {
        sendMessage();
      }
    }
  };

  return (
    <div className="flex flex-col h-screen bg-[#0f0f11] text-[#e0e0ff]">
      {/* Header */}
      <div className="p-4 border-b border-[#333344]">
        <h1 className="text-xl font-semibold">AI Chat Assistant</h1>
      </div>

      {/* Chat Container */}
      <div
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto p-6 space-y-8"
      >
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-[#888899]">
            <div className="mb-4 text-4xl">🤖</div>
            <h2 className="text-2xl font-light mb-2">Welcome to AI Chat</h2>
            <p className="text-sm max-w-md">Ask me anything! I'm here to help with your questions and tasks.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`max-w-[80%] ${
                message.role === 'user'
                  ? 'ml-auto'
                  : 'mr-auto'
              }`}
            >
              <div className="text-xs opacity-60 mb-1">
                {message.role === 'user' ? 'You' : 'Assistant'}
              </div>
              <div
                className={`p-4 rounded-2xl ${
                  message.role === 'user'
                    ? 'bg-[#2a2a40] rounded-br-sm'
                    : 'bg-[#1e293b] rounded-bl-sm'
                }`}
              >
                {message.content}
              </div>
            </div>
          ))
        )}

        {isLoading && (
          <div className="max-w-[80%] mr-auto">
            <div className="text-xs opacity-60 mb-1">Assistant</div>
            <div className="p-4 bg-[#1e293b] rounded-2xl rounded-bl-sm flex items-center space-x-2">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-[#888] rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-[#888] rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                <div className="w-2 h-2 bg-[#888] rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 bg-[#1a1a20] border-t border-[#333344] sticky bottom-0">
        <div className="max-w-2xl mx-auto relative">
          <textarea
            id="prompt"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything..."
            disabled={isLoading}
            className="w-full min-h-14 max-h-44 p-4 pr-16 bg-[#222233] border border-[#444455] rounded-xl text-white resize-none focus:outline-none focus:ring-2 focus:ring-[#6366f1] focus:border-transparent"
            rows={1}
          />
          <button
            onClick={sendMessage}
            disabled={!inputValue.trim() || isLoading}
            className={`absolute right-3 bottom-3 w-8 h-8 rounded-full flex items-center justify-center text-white transition-all ${
              inputValue.trim() && !isLoading
                ? 'bg-[#6366f1] hover:bg-[#4f46e5] hover:scale-105'
                : 'bg-[#444] cursor-not-allowed'
            }`}
          >
            →
          </button>
        </div>
      </div>
    </div>
  );
}