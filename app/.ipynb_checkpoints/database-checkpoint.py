from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from psycopg2.extras import RealDictCursor
# import time
# import psycopg2

# the below code is required when we need to connect our database using postgres driver, but as we are using sqlorm, this is not required

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='niketh457',
#                                 cursor_factory=RealDictCursor)
#         # RealDictCursor is used to get the column names of the retrived data
#         cursor = conn.cursor()
#         print("Connected to dataBase")
#         break
#     except Exception as error:
#         print("Error :", error)
#         time.sleep(3)

# SQLALCHEMY_DB_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQL_URL = 'postgresql://postgres:niketh457@localhost/postgres'

engine = create_engine(SQL_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
