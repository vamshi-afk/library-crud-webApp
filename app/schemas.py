from pydantic import BaseModel, ConfigDict, Field


class bookBlueprint(BaseModel):
    title: str
    author: str
    total_copies: int = Field(gt=0, description="Must have atleast 1 copy")


class bookResponse(BaseModel):
    id: int
    title: str
    author: str
    total_copies: int
    available_copies: int

    model_config = ConfigDict(from_attributes=True)


class memberBlueprint(BaseModel):
    name: str
    email: str


class memberResponse(BaseModel):
    id: int
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)
