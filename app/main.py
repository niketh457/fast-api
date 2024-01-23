from fastapi import FastAPI
from .models import Base 
from .routers import notes, user, authentication, likes
from .database import engine
from .config import settings

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(notes.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(likes.router)
