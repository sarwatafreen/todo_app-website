'use client';

import React, { useState, useEffect } from 'react';
import ProtectedRoute from '../../components/ProtectedRoute';
import TodoList from '../../components/Todo/TodoList';
import TodoForm from '../../components/Todo/TodoForm';
import ChatInterface from '../../components/Chat/ChatInterface';
import { Todo } from '../../components/Todo/TodoList';
import { todoApiService } from '../../services/api';
import { useAuth } from '../../context/auth-context';

const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch todos when component mounts or when a task update occurs
  const fetchTodos = async () => {
    if (!user?.user_id) return;

    try {
      setLoading(true);
      const userTodos = await todoApiService.getUserTodos(user.user_id);
      setTodos(userTodos);
      setError(null);
    } catch (err) {
      setError('Failed to load todos. Please try again.');
      console.error('Error fetching todos:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch todos on initial load
  useEffect(() => {
    fetchTodos();
  }, [user?.user_id]);

  // Handler to refresh todos after a task operation
  const handleTaskUpdate = () => {
    fetchTodos(); // Refresh the task list
  };

  if (!user) {
    return <div>Redirecting...</div>;
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">Todo Dashboard</h1>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Welcome, {user.email}</span>
            </div>
          </div>
        </header>

        <main className="py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="lg:flex lg:gap-x-8">
              {/* Main Content - Task Management */}
              <div className="lg:w-7/12">
                <div className="bg-white shadow rounded-lg overflow-hidden">
                  <div className="px-6 py-4 border-b border-gray-200">
                    <h2 className="text-xl font-semibold text-gray-800">Your Tasks</h2>
                    <p className="text-sm text-gray-600 mt-1">Manage your tasks efficiently</p>
                  </div>

                  <div className="p-6">
                    <TodoForm userId={user.user_id} onTaskCreated={fetchTodos} />

                    {error && (
                      <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg">
                        {error}
                      </div>
                    )}

                    {loading ? (
                      <div className="flex justify-center items-center h-32">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                        <span className="ml-2">Loading tasks...</span>
                      </div>
                    ) : (
                      <div className="mt-6">
                        <div className="flex justify-between items-center mb-4">
                          <h3 className="text-lg font-medium text-gray-900">Task List</h3>
                          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                            {todos.length} {todos.length === 1 ? 'task' : 'tasks'}
                          </span>
                        </div>

                        <TodoList
                          todos={todos}
                          onTaskUpdated={fetchTodos}
                          onTaskDeleted={fetchTodos}
                        />
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Sidebar - Chat Interface */}
              <div className="lg:w-5/12 mt-8 lg:mt-0">
                <div className="bg-white shadow rounded-lg overflow-hidden h-full">
                  <div className="px-6 py-4 border-b border-gray-200">
                    <h2 className="text-xl font-semibold text-gray-800">AI Todo Assistant</h2>
                    <p className="text-xs text-gray-600 mt-1">Chat naturally to manage your tasks</p>
                  </div>

                  <div className="p-4 h-[calc(100%-5rem)]">
                    <ChatInterface />
                  </div>
                </div>

                {/* Quick Tips */}
                <div className="mt-6 bg-blue-50 p-4 rounded-lg">
                  <h3 className="font-medium text-blue-800 text-sm">Quick Tips:</h3>
                  <ul className="mt-2 text-xs text-blue-700 list-disc pl-5 space-y-1">
                    <li>Add: "Create a task to buy groceries"</li>
                    <li>Update: "Change my meeting to 3 PM"</li>
                    <li>Complete: "Mark shopping as done"</li>
                    <li>List: "Show me my tasks"</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
};

export default DashboardPage;