from contextlib import contextmanager
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://studytracker:studytracker@db:5432/studytracker",
)

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


@contextmanager
def get_session():
    """Yield a SQLAlchemy session with commit/rollback handling.

    Usage pattern in FastAPI routes or services:

        with get_session() as session:
            ...  # use session
    """

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
      
