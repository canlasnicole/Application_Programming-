from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from database import Base


class Rental(Base):
    """📋 rentals 테이블 — Model (SQL 데이터 저장·조회)"""
    __tablename__ = "rentals"

    id          = Column(Integer, primary_key=True, index=True)
    book_id     = Column(Integer, ForeignKey("books.id"), nullable=False)
    member_id   = Column(Integer, ForeignKey("members.id"), nullable=False)
    rented_at   = Column(Date, default=date.today)   # 대출일
    due_date    = Column(Date, nullable=False)         # 반납 예정일
    returned_at = Column(Date, nullable=True)          # 실제 반납일 (None = 미반납)

    book   = relationship("Book",   back_populates="rentals")
    member = relationship("Member", back_populates="rentals")
