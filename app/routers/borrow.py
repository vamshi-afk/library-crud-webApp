from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import BorrowRecord, Book, Member
from app.database import get_db
from app.schemas import BorrowRequest, BorrowResponse

router = APIRouter(prefix="/borrow", tags=["Borrow"])


@router.get("/", response_model=list[BorrowResponse])
def renderBorrowList(db: Session = Depends(get_db)):
    stmt = select(BorrowRecord).order_by(BorrowRecord.id)
    borrow_list = db.scalars(stmt).all()
    return borrow_list


@router.post("/", response_model=BorrowResponse)
def borrowBook(req: BorrowRequest, db: Session = Depends(get_db)):
    book = db.get(Book, req.book_id)
    member = db.get(Member, req.member_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The Book with id {req.book_id} not found",
        )
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The Member with id {req.member_id} not found",
        )
    if book.available_copies == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No Copies available for borrowing",
        )
    borrow_record = db.scalar(
        select(BorrowRecord).where(
            BorrowRecord.book_id == req.book_id,
            BorrowRecord.member_id == req.member_id,
            BorrowRecord.returned_at.is_(None),
        )
    )
    if borrow_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Already Borrowed by you"
        )
    book.available_copies -= 1

    new_borrow_record = BorrowRecord(
        book_id=req.book_id,
        member_id=req.member_id,
    )
    db.add(new_borrow_record)
    db.commit()
    db.refresh(new_borrow_record)
    return new_borrow_record


@router.put("/return/{record_id}", response_model=BorrowResponse)
def returnBook(record_id: int, db: Session = Depends(get_db)):
    record_check = db.get(BorrowRecord, record_id)
    if not record_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the borrow record {record_id} doesnt exist",
        )
    if record_check.returned_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The book has already been returned",
        )
    book = db.get(Book, record_check.book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"The book doesnt exist"
        )
    book.available_copies += 1
    record_check.returned_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(record_check)
    return record_check
