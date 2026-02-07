# Quickstart Guide

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file:
   ```
   DATABASE_URL=postgresql://username:password@localhost/todo_db
   JWT_SECRET_KEY=your-super-secret-key-change-in-production-keep-it-long-and-random
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Start the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

## Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables by creating a `.env.local` file:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   ```

## Running the Application

1. Start the backend server (port 8000)
2. Start the frontend server (port 3000)
3. Visit `http://localhost:3000` in your browser

## Testing the API

You can test the API endpoints directly at `http://localhost:8000/docs` which provides an interactive Swagger UI interface.

## Database Initialization

On first run, the database tables will be automatically created when you start the application. Alternatively, you can run:

```bash
python -c "from src.database.init_db import create_tables; create_tables()"
```

## Security Notes

- All API endpoints require JWT authentication
- Users can only access their own data
- Passwords are securely hashed using bcrypt
- Tokens expire after 30 minutes by default