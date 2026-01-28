import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

# Test the database connection
async def test_connection():
    # Use the same URL format as in your .env file
    database_url = "postgresql+asyncpg://neondb_owner:npg_3nAX0UqcyhrE@ep-ancient-salad-ah3gph2u-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"

    try:
        engine = create_async_engine(database_url)
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")
            print("Connection successful!")
            print(result.fetchone())
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())