from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.schemas import bookBlueprint, bookResponse
from app.database import get_db
from app.models import Book

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[bookResponse])
def renderBooks(db: Session = Depends(get_db)):
    stmt = select(Book).order_by(Book.id)
    books = db.scalars(stmt).all()
    return books


@router.post("/", response_model=bookResponse, status_code=status.HTTP_201_CREATED)
def addBooks(book_in: bookBlueprint, db: Session = Depends(get_db)):
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
def deleteBook(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The Book with id {book_id} not found",
        )
    db.delete(book)
    db.commit()
    return {"message": f"Book '{book.title}' deleted successfully"}
