// API client for the AI Task Agent System
const API_BASE_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

/**
 * Fetch all tasks from the API
 */
export async function fetchTasks() {
  try {
    const response = await fetch(`${API_BASE_URL}/tasks`);
    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching tasks:', error);
    throw error;
  }
}

/**
 * Process text through the AI agent
 */
export async function processWithAgent(text) {
  try {
    const response = await fetch(`${API_BASE_URL}/agent/task`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error(`Agent API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error processing with agent:', error);
    throw error;
  }
}

/**
 * Create a new task via the API
 */
export async function createTask(taskData) {
  try {
    const response = await fetch(`${API_BASE_URL}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error creating task:', error);
    throw error;
  }
}

/**
 * Update an existing task via the API
 */
export async function updateTask(id, taskData) {
  try {
    const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error updating task:', error);
    throw error;
  }
}

/**
 * Delete a task via the API
 */
export async function deleteTask(id) {
  try {
    const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error deleting task:', error);
    throw error;
  }
}