from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# for getting input for the user (Request)

class NoteBase(BaseModel):
    title: str
    note: str
    completed: bool = True
    

class NoteUpdate(NoteBase):
    pass

class User(BaseModel):
    email: EmailStr
    password: str

# for sending output for the user (response)

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True

class NoteResponse(NoteBase):
    id: int
    noted_at: datetime
    user: UserResponse

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    

class Likes(BaseModel):
    note_id: int
    like: bool
