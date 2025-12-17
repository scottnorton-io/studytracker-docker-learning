# 📋 StudyTracker – Database & Models (Copy-Paste Ready)

Copy-paste-ready database and ORM layer for StudyTracker, aligned with the ER diagram (Topic–Session) and the Compose `DATABASE_URL`.

> **Scope:** SQLAlchemy models + DB session helper. This is the v0.2.0 Postgres-backed core that will replace the in-memory lists.
> 

---

## src/app/[database.py](http://database.py)

```python
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
```

---

## src/app/[models.py](http://models.py)

```python
from datetime import datetime, date

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    sessions = relationship("Session", back_populates="topic", cascade="all, delete-orphan")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("[topics.id](http://topics.id)", ondelete="CASCADE"), nullable=False, index=True)
    study_date = Column(Date, nullable=False, default=[date.today](http://date.today))
    duration_minutes = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    topic = relationship("Topic", back_populates="sessions")
```

---

## Minimal migration / bootstrap helper (optional)

```python
# src/app/bootstrap_[db.py](http://db.py)
from app.database import engine
from app.models import Base

def init_db() -> None:
    """Create all tables if they do not exist.

    For local dev and tests; production should use a proper migration tool
    (Alembic) wired into CI/CD.
    """

    Base.metadata.create_all(bind=engine)
```

Run once at startup (e.g., from [`main.py`](http://main.py)) during early development, then replace with migrations in later phases.