from sqlmodel import SQLModel
from .database import engine
from ..models.user import User
from ..models.todo import Todo

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()