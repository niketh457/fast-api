from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, utils, models, outh

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # OAuth2PasswordRequestForm doesn't think of what's the given input. It will return only username and password,
    # So user_credentials.username must be used below and also data should be sent in the form_data format, not in the
    # json format
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    # create Token
    access_token = outh.jwt_token(data={'user_id': user.id})
    # return Token

    return {"access_token": access_token, 'token_type': 'bearer'}
