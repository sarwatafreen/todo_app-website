import React, { useState } from 'react';
import { Todo } from './TodoList';
import { todoApiService } from '../../services/api';

interface TodoItemProps {
  todo: Todo;
  onToggleComplete: (userId: string, taskId: string, currentStatus: boolean) => void;
  onDelete: (userId: string, taskId: string) => void;
  isDeleting: boolean;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggleComplete, onDelete, isDeleting }) => {
  const [showConfirm, setShowConfirm] = useState(false);

  const handleToggle = () => {
    onToggleComplete(todo.owner_id, todo.id, todo.is_completed);
  };

  const handleDeleteClick = () => {
    if (showConfirm) {
      onDelete(todo.owner_id, todo.id);
      setShowConfirm(false);
    } else {
      setShowConfirm(true);
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  return (
    <div className={`border rounded-lg p-4 transition-all ${todo.is_completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'}`}>
      <div className="flex items-start">
        <input
          type="checkbox"
          checked={todo.is_completed}
          onChange={handleToggle}
          className="mt-1 h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
        />
        <div className="ml-3 flex-1">
          <div className="flex justify-between">
            <h3 className={`text-sm font-medium ${todo.is_completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {todo.title}
            </h3>
            <div className="flex space-x-2">
              {todo.due_date && (
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                  Due: {formatDate(todo.due_date)}
                </span>
              )}
              {todo.is_completed && (
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Completed
                </span>
              )}
            </div>
          </div>

          {todo.description && (
            <p className="mt-1 text-sm text-gray-600">{todo.description}</p>
          )}

          <div className="mt-2 text-xs text-gray-500">
            Created: {formatDate(todo.created_at)}
          </div>
        </div>
      </div>

      <div className="mt-3 flex justify-end">
        {showConfirm ? (
          <div className="flex space-x-2">
            <button
              onClick={() => setShowConfirm(false)}
              className="text-xs bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded"
            >
              Cancel
            </button>
            <button
              onClick={handleDeleteClick}
              disabled={isDeleting}
              className="text-xs bg-red-600 hover:bg-red-700 text-white py-1 px-2 rounded disabled:opacity-50"
            >
              {isDeleting ? 'Deleting...' : 'Confirm Delete'}
            </button>
          </div>
        ) : (
          <button
            onClick={handleDeleteClick}
            disabled={isDeleting}
            className="text-xs bg-red-100 hover:bg-red-200 text-red-700 py-1 px-2 rounded disabled:opacity-50"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  );
};

export default TodoItem;