from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from rentals.schemas import RentalCreate, RentalResponse
import rentals.crud as crud

router = APIRouter(prefix="/api/rentals", tags=["Rentals"])


@router.post("/", response_model=RentalResponse)
def borrow_book(rental: RentalCreate, db: Session = Depends(get_db)):
    """책 대출"""
    result = crud.create_rental(db, rental)
    if isinstance(result, str):
        raise HTTPException(status_code=400, detail=result)
    return result


@router.patch("/{rental_id}/return", response_model=RentalResponse)
def return_book(rental_id: int, db: Session = Depends(get_db)):
    """책 반납"""
    result = crud.return_book(db, rental_id)
    if isinstance(result, str):
        raise HTTPException(status_code=400, detail=result)
    return result


@router.get("/", response_model=list[RentalResponse])
def get_rentals(db: Session = Depends(get_db)):
    """전체 대출 기록"""
    return crud.get_rentals(db)


@router.get("/overdue", response_model=list[RentalResponse])
def get_overdue(db: Session = Depends(get_db)):
    """연체 목록"""
    return crud.get_overdue(db)


@router.delete("/{rental_id}")
def delete_rental(rental_id: int, db: Session = Depends(get_db)):
    """대출 기록 삭제"""
    if not crud.delete_rental(db, rental_id):
        raise HTTPException(status_code=404, detail="대출 기록을 찾을 수 없습니다.")
    return {"msg": "대출 기록이 삭제되었습니다."}
