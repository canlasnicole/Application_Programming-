from sqlalchemy.orm import Session
from datetime import date
from rentals.models import Rental
from rentals.schemas import RentalCreate
from books.models import Book


def create_rental(db: Session, rental: RentalCreate) -> Rental | str:
    book = db.query(Book).filter(Book.id == rental.book_id).first()
    if not book:
        return "책을 찾을 수 없습니다."
    if not book.is_available:
        return "이미 대출 중인 책입니다."
    db_rental = Rental(
        book_id=rental.book_id,
        member_id=rental.member_id,
        rented_at=date.today(),
        due_date=rental.due_date,
    )
    db.add(db_rental)
    book.is_available = False
    db.commit()
    db.refresh(db_rental)
    return db_rental


def return_book(db: Session, rental_id: int) -> Rental | str:
    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if not rental:
        return "대출 기록을 찾을 수 없습니다."
    if rental.returned_at:
        return "이미 반납된 책입니다."
    rental.returned_at = date.today()
    rental.book.is_available = True
    db.commit()
    db.refresh(rental)
    return rental


def get_rentals(db: Session) -> list[Rental]:
    return db.query(Rental).all()


def get_overdue(db: Session) -> list[Rental]:
    return db.query(Rental).filter(
        Rental.returned_at == None,
        Rental.due_date < date.today()
    ).all()


def delete_rental(db: Session, rental_id: int) -> bool:
    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if not rental:
        return False
    if not rental.returned_at:
        rental.book.is_available = True
    db.delete(rental)
    db.commit()
    return True
