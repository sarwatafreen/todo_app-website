import { NextRequest, NextResponse } from 'next/server';

// Define the Task interface here to avoid circular imports
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

const BACKEND_API_URL = process.env.BACKEND_API_URL || 'http://localhost:8000/api';

// Dynamic segment for task ID
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const awaitedParams = await params;
    const { id } = awaitedParams;

    const response = await fetch(`${BACKEND_API_URL}/tasks/${id}`);

    if (!response.ok) {
      if (response.status === 404) {
        return NextResponse.json(
          { error: { code: 'NOT_FOUND', message: 'Task not found' } },
          { status: 404 }
        );
      }
      throw new Error(`Backend API error: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching task:', error);
    return NextResponse.json(
      { error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch task' } },
      { status: 500 }
    );
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const awaitedParams = await params;
    const { id } = awaitedParams;
    const body = await request.json();

    const response = await fetch(`${BACKEND_API_URL}/tasks/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return NextResponse.json(errorData, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error updating task:', error);
    return NextResponse.json(
      { error: { code: 'INTERNAL_ERROR', message: 'Failed to update task' } },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const awaitedParams = await params;
    const { id } = awaitedParams;

    const response = await fetch(`${BACKEND_API_URL}/tasks/${id}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const errorData = await response.json();
      return NextResponse.json(errorData, { status: response.status });
    }

    return NextResponse.json({ message: 'Task deleted successfully' });
  } catch (error) {
    console.error('Error deleting task:', error);
    return NextResponse.json(
      { error: { code: 'INTERNAL_ERROR', message: 'Failed to delete task' } },
      { status: 500 }
    );
  }
}

// Separate route for toggling completion status
export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const awaitedParams = await params;
    const { id } = awaitedParams;

    const response = await fetch(`${BACKEND_API_URL}/tasks/${id}/toggle`, {
      method: 'PATCH',
    });

    if (!response.ok) {
      const errorData = await response.json();
      return NextResponse.json(errorData, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error toggling task completion:', error);
    return NextResponse.json(
      { error: { code: 'INTERNAL_ERROR', message: 'Failed to toggle task completion' } },
      { status: 500 }
    );
  }
}