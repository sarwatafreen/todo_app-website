import { NextRequest, NextResponse } from 'next/server';

// This is a proxy route to connect the Next.js frontend to the FastAPI backend
const BACKEND_API_URL = process.env.BACKEND_API_URL || 'http://localhost:8000/api';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const search = searchParams.get('search');
    const completed = searchParams.get('completed');
    const priority = searchParams.get('priority');
    const tag = searchParams.get('tag');
    const sort = searchParams.get('sort');
    const order = searchParams.get('order');
    const page = searchParams.get('page');
    const limit = searchParams.get('limit');

    // Construct query parameters for backend API
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (completed) params.append('completed', completed);
    if (priority) params.append('priority', priority);
    if (tag) params.append('tag', tag);
    if (sort) params.append('sort', sort);
    if (order) params.append('order', order);
    if (page) params.append('page', page);
    if (limit) params.append('limit', limit);

    const response = await fetch(`${BACKEND_API_URL}/tasks?${params.toString()}`);

    if (!response.ok) {
      console.error(`Backend API error: ${response.status}`);
      // Return empty array on error to prevent frontend from breaking
      return NextResponse.json([], { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching tasks:', error);
    // Return empty array on error to prevent frontend from breaking
    return NextResponse.json([], { status: 200 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const response = await fetch(`${BACKEND_API_URL}/tasks`, {
      method: 'POST',
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
    return NextResponse.json(data, { status: 201 });
  } catch (error) {
    console.error('Error creating task:', error);
    return NextResponse.json(
      { error: { code: 'INTERNAL_ERROR', message: 'Failed to create task' } },
      { status: 500 }
    );
  }
}