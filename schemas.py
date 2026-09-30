from pydantic import BaseModel, Field


class Job(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    company: str = Field(min_length=2, max_length=100)
    location: str
    salary: int = Field(gt=0)
    status: str = "applied"


class UserCreate(BaseModel):
    email: str
    password: str