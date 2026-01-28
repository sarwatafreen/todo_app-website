'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/auth-context';
import { todoApiService } from '@/services/api';

interface Todo {
  id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
  due_date?: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout, isAuthenticated } = useAuth();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Check if user is authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    } else {
      loadTodos();
    }
  }, [isAuthenticated, router]);

  const loadTodos = async () => {
    try {
      setLoading(true);
      if (!user) {
        router.push('/login');
        return;
      }

      const userTodos = await todoApiService.getUserTodos(user.user_id);
      setTodos(userTodos);
    } catch (err: any) {
      setError(err.message || 'Failed to load todos');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTodo.trim()) return;

    try {
      if (!user) {
        router.push('/login');
        return;
      }

      const todoData = {
        title: newTodo,
        description: newDescription || undefined,
      };

      const newTodoItem = await todoApiService.createTodo(user.user_id, todoData);
      setTodos([newTodoItem, ...todos]);
      setNewTodo('');
      setNewDescription('');
    } catch (err: any) {
      setError(err.message || 'Failed to add todo');
    }
  };

  const toggleTodo = async (todo: Todo) => {
    try {
      if (!user) {
        router.push('/login');
        return;
      }

      const updatedTodo = await todoApiService.toggleTodoCompletion(
        user.user_id,
        todo.id,
        !todo.is_completed
      );

      setTodos(todos.map(t => t.id === todo.id ? updatedTodo : t));
    } catch (err: any) {
      setError(err.message || 'Failed to update todo');
    }
  };

  const deleteTodo = async (todoId: string) => {
    try {
      if (!user) {
        router.push('/login');
        return;
      }

      await todoApiService.deleteTodo(user.user_id, todoId);
      setTodos(todos.filter(todo => todo.id !== todoId));
    } catch (err: any) {
      setError(err.message || 'Failed to delete todo');
    }
  };

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[80vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Your Todos</h1>
          <p className="text-sm text-gray-600 mt-1">
            Also accessible at <a href="/tasks" className="text-blue-600 hover:underline">/tasks</a>
          </p>
        </div>
        <button
          onClick={handleLogout}
          className="text-sm font-medium text-red-600 hover:text-red-500"
        >
          Logout
        </button>
      </div>

      {error && (
        <div className="mb-4 text-red-600 text-sm">
          {error}
        </div>
      )}

      {/* Add Todo Form */}
      <form onSubmit={handleAddTodo} className="mb-8 bg-white p-6 rounded-lg shadow">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="md:col-span-2">
            <input
              type="text"
              value={newTodo}
              onChange={(e) => setNewTodo(e.target.value)}
              placeholder="What needs to be done?"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              required
            />
          </div>
          <div className="md:col-span-1">
            <input
              type="text"
              value={newDescription}
              onChange={(e) => setNewDescription(e.target.value)}
              placeholder="Description (optional)"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div className="md:col-span-1">
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Add Todo
            </button>
          </div>
        </div>
      </form>

      {/* Todo List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {todos.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <p>No todos yet. Add your first todo above!</p>
          </div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {todos.map((todo) => (
              <li key={todo.id} className="p-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      checked={todo.is_completed}
                      onChange={() => toggleTodo(todo)}
                      className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span
                      className={`ml-3 text-lg ${
                        todo.is_completed ? 'line-through text-gray-500' : 'text-gray-900'
                      }`}
                    >
                      {todo.title}
                    </span>
                  </div>
                  <div className="flex items-center space-x-4">
                    {todo.description && (
                      <span className="text-sm text-gray-500">{todo.description}</span>
                    )}
                    <button
                      onClick={() => deleteTodo(todo.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </div>
                </div>
                {todo.due_date && (
                  <div className="ml-7 mt-1 text-sm text-gray-500">
                    Due: {new Date(todo.due_date).toLocaleDateString()}
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}