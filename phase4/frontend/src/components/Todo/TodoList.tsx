import React from 'react';
import TodoItem from './TodoItem';
import { todoApiService } from '../../services/api';

export interface Todo {
  id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  owner_id: string;
  created_at: string;
  updated_at: string;
  due_date?: string;
}

interface TodoListProps {
  todos: Todo[];
  onTaskUpdated?: () => void;
  onTaskDeleted?: () => void;
}

const TodoList: React.FC<TodoListProps> = ({ todos, onTaskUpdated, onTaskDeleted }) => {
  const handleToggleComplete = async (userId: string, taskId: string, currentStatus: boolean) => {
    try {
      await todoApiService.toggleTodoCompletion(userId, taskId, !currentStatus);
      if (onTaskUpdated) onTaskUpdated();
    } catch (error) {
      console.error('Error toggling task completion:', error);
    }
  };

  const handleDelete = async (userId: string, taskId: string) => {
    try {
      await todoApiService.deleteTodo(userId, taskId);
      if (onTaskDeleted) onTaskDeleted();
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  if (todos.length === 0) {
    return (
      <div className="text-center py-8">
        <div className="text-gray-500 mb-2">No tasks found</div>
        <p className="text-sm text-gray-400">Add a task to get started</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggleComplete={handleToggleComplete}
          onDelete={handleDelete}
          isDeleting={false}
        />
      ))}
    </div>
  );
};

export default TodoList;