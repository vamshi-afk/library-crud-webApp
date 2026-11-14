from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.schemas import memberBlueprint, memberResponse
from app.database import get_db
from app.models import Member

router = APIRouter(prefix="/members", tags=["Members"])


@router.get("/", response_model=list[memberResponse])
def renderMembers(db: Session = Depends(get_db)):
    stmt = select(Member).order_by(Member.id)
    members = db.scalars(stmt).all()
    return members


@router.post("/", response_model=memberResponse, status_code=status.HTTP_201_CREATED)
def addMembers(member: memberBlueprint, db: Session = Depends(get_db)):
    new_member = Member(
        name=member.name,
        email=member.email,
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@router.delete("/{member_id}")
def removeMembers(member_id: int, db: Session = Depends(get_db)):
    member = db.get(Member, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found",
        )
    db.delete(member)
    db.commit()
    return {"message": "Member '{member.name}' was removed"}
