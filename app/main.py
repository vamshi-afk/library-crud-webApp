from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

books_db = []


class book_blueprint(BaseModel):
    title: str
    author: str
    total_copies: int


@app.get("/books")
def renderBooks():
    return books_db


@app.post("/books")
def addBook(book: book_blueprint):
    new_book = {
        "id": len(books_db) + 1,
        "title": book.title,
        "author": book.author,
        "total_copies": book.total_copies,
        "available_copies": book.total_copies,
    }
    books_db.append(new_book)
    return new_book


@app.delete("/books/{book_id}")
def deleteBook(book_id: int):
    if book_id:
        for index, book in enumerate(books_db):
            if book["id"] == book_id:
                books_db.pop(index)
                return {"message": f"Book '{book['title']}' deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {book_id} not found",
    )


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})
