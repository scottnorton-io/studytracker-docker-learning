from datetime import datetime, date
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable message")
    field: Optional[str] = Field(None, description="Field or parameter involved, if applicable")


class ErrorEnvelope(BaseModel):
    trace_id: Optional[str] = Field(None, description="Trace or correlation ID")
    error: ErrorDetail
    details: Optional[Dict[str, Any]] = None


class TopicBase(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None


class TopicCreate(TopicBase):
    pass


class TopicRead(TopicBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    topic_id: int
    study_date: date
    duration_minutes: int = Field(..., ge=1, le=1440)
    notes: Optional[str] = None


class SessionCreate(SessionBase):
    pass


class SessionRead(SessionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TopicWithSessions(TopicRead):
    sessions: List[SessionRead] = []
  
