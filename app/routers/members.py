from fastapi import APIRouter, HTTPException, status

from app.schemas import memberBlueprint

router = APIRouter(prefix="/members", tags=["Members"])

members_db = []


@router.get("/")
def renderMembers():
    return members_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def addMembers(member: memberBlueprint):
    new_entry = {
        "id": len(members_db) + 1,
        "name": member.name,
        "email": member.email,
    }
    members_db.append(new_entry)
    return new_entry


@router.delete("/{member_id}")
def removeMembers(member_id: int):
    for index, member in enumerate(members_db):
        if member["id"] == member_id:
            members_db.pop(index)
            return {"message": f"Member {member['name']} removed successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Member with id {member_id} not found",
    )
