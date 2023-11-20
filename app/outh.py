from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def jwt_token(data: dict):
    req = data.copy()

    EXPIRE_TIME = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    req['exp'] = EXPIRE_TIME

    encoded_jwt = jwt.encode(req, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
