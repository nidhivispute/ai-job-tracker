from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


JobStatus = Literal[
    "saved",
    "applied",
    "interviewing",
    "offer",
    "rejected",
    "withdrawn",
]


class JobCreate(BaseModel):
    company_name: str = Field(min_length=1, max_length=255)
    job_title: str = Field(min_length=1, max_length=255)
    job_description: str | None = None
    job_url: str | None = None
    location: str | None = None
    status: JobStatus = "saved"


class JobUpdate(BaseModel):
    company_name: str | None = Field(default=None, min_length=1, max_length=255)
    job_title: str | None = Field(default=None, min_length=1, max_length=255)
    job_description: str | None = None
    job_url: str | None = None
    location: str | None = None
    status: JobStatus | None = None


class JobRead(BaseModel):
    id: int
    user_id: int
    company_name: str
    job_title: str
    job_description: str | None
    job_url: str | None
    location: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }