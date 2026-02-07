from sqlmodel import create_engine, Session
from typing import Generator
from src.settings import settings


# Create sync engine for local SQLite
engine = create_engine(settings.database_url, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session