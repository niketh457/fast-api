from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import schemas, models, database
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from .config import settings


# token_Url is the endpoint by which a user logins to his account
outh_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def jwt_token(data: dict):
    req = data.copy()

    EXPIRE_TIME = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    req['exp'] = EXPIRE_TIME

    encoded_jwt = jwt.encode(req, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        pay_load = jwt.decode(token, SECRET_KEY, [ALGORITHM])

        user_id: int = pay_load.get('user_id')

        if user_id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(outh_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Couldn't validate credentials",
                                         headers={'WWW-Authenticate': 'Bearer'})

    user_token = verify_access_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == user_token.id).first()

    return user


