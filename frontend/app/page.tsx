'use client'

import { useState, useEffect } from 'react'

// Define TypeScript interfaces
interface Task {
  id: string
  title: string
  description?: string
  completed: boolean
  priority: 'LOW' | 'MEDIUM' | 'HIGH'
  tags: string[]
  created_at: string
  updated_at: string
}

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [newTask, setNewTask] = useState<{ title: string; description: string; priority: Task['priority']; tags: string }>({ title: '', description: '', priority: 'MEDIUM', tags: '' })

  // Load tasks from API
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch('/api/tasks')

        // Check if response is ok, but handle errors gracefully
        if (!response.ok) {
          console.error(`API error! status: ${response.status}`)
          // Instead of throwing, try to get the response data
          try {
            const errorData = await response.json()
            console.error('API error response:', errorData)
            // Set to empty array if there's an error
            setTasks([])
          } catch (jsonError) {
            // If we can't parse the error response, still set to empty array
            console.error('Could not parse error response:', jsonError)
            setTasks([])
          }
        } else {
          const data = await response.json()

          // Ensure data is an array before setting tasks
          if (Array.isArray(data)) {
            setTasks(data)
          } else {
            console.error('API did not return an array:', data)
            setTasks([]) // Set to empty array as fallback
          }
        }
      } catch (error) {
        console.error('Error fetching tasks:', error)
        setTasks([]) // Set to empty array as fallback on error
      } finally {
        setLoading(false)
      }
    }

    fetchTasks()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Parse tags from comma-separated string
    const tagsArray = newTask.tags.split(',').map(tag => tag.trim()).filter(tag => tag)

    try {
      const response = await fetch('/api/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: newTask.title,
          description: newTask.description,
          priority: newTask.priority,
          tags: tagsArray
        }),
      })

      if (response.ok) {
        const createdTask = await response.json()
        setTasks([...tasks, createdTask])
        setNewTask({ title: '', description: '', priority: 'MEDIUM', tags: '' })
      }
    } catch (error) {
      console.error('Error creating task:', error)
    }
  }

  if (loading) {
    return <div className="container mx-auto p-4">Loading tasks...</div>
  }

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">Task Management</h1>

      {/* Add Task Form */}
      <form onSubmit={handleSubmit} className="mb-8 p-4 border rounded-lg bg-gray-50">
        <h2 className="text-xl font-semibold mb-4">Add New Task</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="title" className="block text-sm font-medium mb-1">Title *</label>
            <input
              type="text"
              id="title"
              value={newTask.title}
              onChange={(e) => setNewTask({...newTask, title: e.target.value})}
              className="w-full px-3 py-2 border rounded-md"
              required
            />
          </div>

          <div>
            <label htmlFor="priority" className="block text-sm font-medium mb-1">Priority</label>
            <select
              id="priority"
              value={newTask.priority}
              onChange={(e) => setNewTask({...newTask, priority: e.target.value as Task['priority']})}
              className="w-full px-3 py-2 border rounded-md"
            >
              <option value="LOW">Low</option>
              <option value="MEDIUM">Medium</option>
              <option value="HIGH">High</option>
            </select>
          </div>

          <div className="md:col-span-2">
            <label htmlFor="description" className="block text-sm font-medium mb-1">Description</label>
            <textarea
              id="description"
              value={newTask.description}
              onChange={(e) => setNewTask({...newTask, description: e.target.value})}
              className="w-full px-3 py-2 border rounded-md"
              rows={2}
            />
          </div>

          <div className="md:col-span-2">
            <label htmlFor="tags" className="block text-sm font-medium mb-1">Tags (comma-separated)</label>
            <input
              type="text"
              id="tags"
              value={newTask.tags}
              onChange={(e) => setNewTask({...newTask, tags: e.target.value})}
              className="w-full px-3 py-2 border rounded-md"
              placeholder="work, personal, urgent..."
            />
          </div>
        </div>

        <button
          type="submit"
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Add Task
        </button>
      </form>

      {/* Task List */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Tasks ({tasks.length})</h2>

        {tasks.length === 0 ? (
          <p>No tasks found.</p>
        ) : (
          <div className="space-y-3">
            {tasks.map((task) => (
              <div
                key={task.id}
                className={`p-4 border rounded-lg ${task.completed ? 'bg-green-50' : 'bg-white'} ${task.priority === 'HIGH' ? 'border-red-200' : task.priority === 'MEDIUM' ? 'border-yellow-200' : 'border-green-200'}`}
              >
                <div className="flex justify-between items-start">
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={async () => {
                        try {
                          const response = await fetch(`/api/tasks/${task.id}/toggle`, {
                            method: 'PATCH',
                          })

                          if (response.ok) {
                            setTasks(tasks.map(t =>
                              t.id === task.id ? {...t, completed: !t.completed} : t
                            ))
                          }
                        } catch (error) {
                          console.error('Error toggling task:', error)
                        }
                      }}
                      className="mr-3 h-4 w-4"
                    />
                    <div>
                      <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : ''}`}>
                        {task.title}
                      </h3>
                      {task.description && (
                        <p className="text-gray-600 mt-1">{task.description}</p>
                      )}

                      <div className="flex flex-wrap gap-2 mt-2">
                        <span className={`px-2 py-1 text-xs rounded ${
                          task.priority === 'HIGH' ? 'bg-red-100 text-red-800' :
                          task.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {task.priority}
                        </span>

                        {task.tags && task.tags.map((tag, index) => (
                          <span key={index} className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="flex space-x-2">
                    <button
                      onClick={async () => {
                        try {
                          const response = await fetch(`/api/tasks/${task.id}`, {
                            method: 'DELETE',
                          })

                          if (response.ok) {
                            setTasks(tasks.filter(t => t.id !== task.id))
                          }
                        } catch (error) {
                          console.error('Error deleting task:', error)
                        }
                      }}
                      className="px-3 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200 text-sm"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}