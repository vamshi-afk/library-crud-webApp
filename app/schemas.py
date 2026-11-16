from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookBlueprint(BaseModel):
    title: str
    author: str
    total_copies: int = Field(gt=0, description="Must have atleast 1 copy")


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    total_copies: int
    available_copies: int
    model_config = ConfigDict(from_attributes=True)


class MemberBlueprint(BaseModel):
    name: str
    email: str


class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class MemberPublic(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class BorrowRequest(BaseModel):
    book_id: int
    member_id: int


class BorrowResponse(BaseModel):
    id: int
    book_id: int
    member_id: int
    borrowed_at: datetime
    returned_at: datetime | None
    book: BookResponse
    member: MemberPublic
    due_date: datetime
    fine: int
    model_config = ConfigDict(from_attributes=True)
