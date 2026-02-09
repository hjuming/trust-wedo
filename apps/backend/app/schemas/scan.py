from pydantic import BaseModel, HttpUrl
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any

class ScanCreate(BaseModel):
    url: HttpUrl

class ScanResponse(BaseModel):
    id: UUID
    user_id: UUID
    url: str
    status: str
    result: Optional[Dict[str, Any]]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
