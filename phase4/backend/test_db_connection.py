from src.database.init_db import create_tables

if __name__ == "__main__":
    print("Testing database connection and initializing tables...")
    try:
        create_tables()
        print("✓ Database connection successful and tables created!")
    except Exception as e:
        print(f"✗ Error connecting to database: {e}")
        raise