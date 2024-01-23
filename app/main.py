from fastapi import FastAPI
from . import models
from .routers import notes, user, authentication
from .database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Even though we use an orm to connect with the database we also need the driver to
# connect to the server, therefore psycopg is must for postgres
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='niketh457',
                                cursor_factory=RealDictCursor)
        # RealDictCursor is used to get the column names of the retrived data
        cursor = conn.cursor()
        print("Connected to dataBase")
        break
    except Exception as error:
        print("Error :", error)
        time.sleep(3)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(notes.router)
app.include_router(user.router)
app.include_router(authentication.router)
