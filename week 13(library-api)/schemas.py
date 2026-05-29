from pydantic import BaseModel
from datetime import date
from typing import Optional


class RentalCreate(BaseModel):
    """POST /api/rentals/ 요청 바디"""
    book_id:   int
    member_id: int
    due_date:  date


class RentalResponse(BaseModel):
    id:          int
    book_id:     int
    member_id:   int
    rented_at:   date
    due_date:    date
    returned_at: Optional[date] = None

    class Config:
        from_attributes = True
