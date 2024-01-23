from fastapi import FastAPI
from . import models 
from .routers import notes, user, authentication
from .database import engine
from pydantic_settings import BaseSettings

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

class Settings(BaseSettings):
    temp: int

settings = Settings()

print(settings.temp)

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(notes.router)
app.include_router(user.router)
app.include_router(authentication.router)
