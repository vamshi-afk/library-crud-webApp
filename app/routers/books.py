from fastapi import APIRouter, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError

from app.database import DbSession
from app.models import Book, BorrowRecord
from app.schemas import BookBlueprint, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[BookResponse])
def renderBooks(search: str, db: DbSession):
    stmt = select(Book).order_by(Book.id)
    if search:
        stmt = stmt.where(
            or_(Book.title.ilike(f"%{search}%"), Book.author.ilike(f"%{search}%"))
        )
    return db.scalars(stmt).all()


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def addBooks(book_in: BookBlueprint, db: DbSession):
    new_book = Book(
        title=book_in.title,
        author=book_in.author,
        total_copies=book_in.total_copies,
        available_copies=book_in.total_copies,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.delete("/{book_id}")
def deleteBook(book_id: int, db: DbSession):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The Book with id {book_id} not found",
        )
    borrow_record = db.scalar(
        select(BorrowRecord).where(
            BorrowRecord.book_id == book_id, BorrowRecord.returned_at.is_(None)
        )
    )
    if borrow_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete the book while copies are currently checked out",
        )
    db.delete(book)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Books with borrow records cannot be deleted",
        ) from None
    return {"message": f"Book '{book.title}' deleted successfully"}
