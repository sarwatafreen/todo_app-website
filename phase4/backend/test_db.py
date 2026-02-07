import asyncio
from src.database import async_engine

async def test_db_connection():
    try:
        async with async_engine.connect() as conn:
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_db_connection())