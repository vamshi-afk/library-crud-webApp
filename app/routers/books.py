from fastapi import HTTPException, APIRouter, status

from app.schemas import bookBlueprint

router = APIRouter(prefix="/books", tags=["Books"])

books_db = []


@router.get("/")
def renderBooks():
    return books_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def addBooks(book: bookBlueprint):
    new_entry = {
        "id": len(books_db) + 1,
        "title": book.title,
        "author": book.author,
        "total_copies": book.total_copies,
        "available_copies": book.total_copies,
    }
    books_db.append(new_entry)
    return new_entry


@router.delete("/{book_id}")
def deleteBook(book_id: int):
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            books_db.pop(index)
            return {"message": f"The Book {book['title']} has been deleted"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The Book with id {book_id} not found",
    )
