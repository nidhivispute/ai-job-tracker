from datetime import datetime

from pydantic import BaseModel


class ResumeRead(BaseModel):
    id: int
    user_id: int
    title: str
    original_filename: str
    stored_filename: str
    file_path: str
    content_type: str
    file_size: int
    extracted_text: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }