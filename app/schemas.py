from pydantic import BaseModel, Field


class bookBlueprint(BaseModel):
    title: str
    author: str
    total_copies: int = Field(gt=0, description="Must have atleast 1 copy")


class memberBlueprint(BaseModel):
    name: str
    email: str
