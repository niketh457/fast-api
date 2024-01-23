from fastapi import FastAPI
from .models import Base 
from .routers import notes, user, authentication, likes
from .database import engine
from .config import settings

from fastapi.middleware.cors import CORSMiddleware

# Base.metadata.create_all(bind=engine)
# The above commad tells sql_alchemy to create the tables with the names mentioned in models.py file
#  as we use data-migration tool it is not necessery now.

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(notes.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(likes.router)
