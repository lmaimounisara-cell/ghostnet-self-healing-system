from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    priority: int = Field(ge=1, le=5, default=3)
    email: str = Field(
        max_length=254,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )


class JobRead(JobCreate):
    id: int
    status: str