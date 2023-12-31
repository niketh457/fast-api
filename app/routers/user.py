from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session

from .. import models, utils
from ..database import get_db
from ..schemas import UserResponse, User

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: User, db: Session = Depends(get_db)):

    user.password = utils.strong_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(path='/{id}', response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} doesnt exist')

    return user
