# src/app/bootstrap_db.py
from app.database import engine
from app.models import Base


def init_db() -> None:
    """Create all tables if they do not exist.

    For local dev and tests; production should use a proper migration tool
    (Alembic) wired into CI/CD.
    """

    Base.metadata.create_all(bind=engine)
