from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import DbSession
from app.models import BorrowRecord, Member
from app.schemas import MemberBlueprint, MemberResponse

router = APIRouter(prefix="/members", tags=["Members"])


@router.get("/", response_model=list[MemberResponse])
def renderMembers(db: DbSession):
    stmt = select(Member).order_by(Member.id)
    members = db.scalars(stmt).all()
    return members


@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def addMembers(member: MemberBlueprint, db: DbSession):
    stmt = select(Member).where(Member.email == member.email)
    existingMail = db.scalar(stmt)
    if existingMail:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The email {member.email} already exists",
        )
    new_member = Member(
        name=member.name,
        email=member.email,
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@router.delete("/{member_id}")
def removeMembers(member_id: int, db: DbSession):
    member = db.get(Member, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found",
        )
    borrow_record = db.scalar(
        select(BorrowRecord).where(
            BorrowRecord.member_id == member_id, BorrowRecord.returned_at.is_(None)
        )
    )
    if borrow_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove a member who has borrowed a copy",
        )
    db.delete(member)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="member with borrow history cannot be deleted",
        ) from None
    return {"message": f"Member '{member.name}' was removed"}
