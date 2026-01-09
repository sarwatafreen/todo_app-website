from sqlmodel import create_engine, Session
from contextlib import contextmanager
import os


DATABASE_URL = os.getenv("NEON_DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, echo=True)


@contextmanager
def get_session_context():
    with Session(engine) as session:
        yield session


def get_session():
    with Session(engine) as session:
        yield session