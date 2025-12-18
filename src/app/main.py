from contextlib import contextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Topic as TopicModel, Session as SessionModel
from app.schemas import (
    ErrorDetail,
    ErrorEnvelope,
    SessionCreate,
    SessionRead,
    TopicCreate,
    TopicRead,
    TopicWithSessions,
)


app = FastAPI(title="StudyTracker")


# --- DB session dependency -------------------------------------------------

@contextmanager
def _session_scope() -> Session:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db():
    with _session_scope() as session:
        yield session


# --- Error handling ---------------------------------------------------------

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    trace_id = request.headers.get("X-Trace-Id")
    # Map HTTPException to a generic error envelope; codes can be refined later
    code = "HTTP_" + str(exc.status_code)
    envelope = ErrorEnvelope(
        trace_id=trace_id,
        error=ErrorDetail(code=code, message=exc.detail or "HTTP error"),
    )
    return JSONResponse(status_code=exc.status_code, content=envelope.dict())


# --- Health -----------------------------------------------------------------

@app.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok", "service": "studytracker-web-fastapi"}


# --- Topics -----------------------------------------------------------------

@app.get("/topics", response_model=List[TopicRead])
async def list_topics(db: Session = Depends(get_db)):
    rows = db.query(TopicModel).order_by(TopicModel.created_at.desc()).all()
    return rows


@app.post("/topics", response_model=TopicRead, status_code=201)
async def create_topic(payload: TopicCreate, db: Session = Depends(get_db)):
    topic = TopicModel(name=payload.name, description=payload.description)
    db.add(topic)
    db.flush()  # populate PK
    db.refresh(topic)
    return topic


@app.get("/topics/{topic_id}", response_model=TopicWithSessions)
async def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = (
        db.query(TopicModel)
        .filter(TopicModel.id == topic_id)
        .first()
    )
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    # SQLAlchemy relationship will load sessions as needed
    return topic


# --- Sessions ---------------------------------------------------------------

@app.post("/sessions", response_model=SessionRead, status_code=201)
async def create_session(payload: SessionCreate, db: Session = Depends(get_db)):
    # Ensure topic exists
    topic = (
        db.query(TopicModel)
        .filter(TopicModel.id == payload.topic_id)
        .first()
    )
    if not topic:
        raise HTTPException(status_code=400, detail="Unknown topic_id")

    session_obj = SessionModel(
        topic_id=payload.topic_id,
        study_date=payload.study_date,
        duration_minutes=payload.duration_minutes,
        notes=payload.notes,
    )
    db.add(session_obj)
    db.flush()
    db.refresh(session_obj)
    return session_obj
