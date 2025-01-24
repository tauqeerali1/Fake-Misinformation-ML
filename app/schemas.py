from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    average_stars: float
    total_reviews: int

    class Config:
        from_attributes = True

class ReviewHistoryBase(BaseModel):
    text: Optional[str] = None
    stars: int = Field(..., ge=1, le=10)
    review_id: str = Field(..., max_length=255)
    tone: Optional[str] = None
    sentiment: Optional[str] = None
    category_id: int

class ReviewHistoryResponse(ReviewHistoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AccessLogCreate(BaseModel):
    text: str