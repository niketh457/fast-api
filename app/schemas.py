from datetime import datetime

from pydantic import BaseModel, EmailStr


# for getting input for the user (Request)

class NoteBase(BaseModel):
    title: str
    note: str
    completed: bool = True


class NoteUpdate(NoteBase):
    pass


# for sending output for the user (response)

class NoteResponse(NoteBase):
    id: int
    noted_at: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True
