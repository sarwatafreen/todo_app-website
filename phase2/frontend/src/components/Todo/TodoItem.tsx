import React from 'react';

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

interface TodoItemProps {
  todo: Todo;
  onToggle: (todo: Todo) => void;
  onDelete: (id: string) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle, onDelete }) => {
  return (
    <li className="p-4 hover:bg-gray-50">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={todo.is_completed}
            onChange={() => onToggle(todo)}
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
            onClick={() => onDelete(todo.id)}
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
  );
};

export default TodoItem;