from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, schemas, outh, models


router = APIRouter(
    prefix='/likes',
    tags=['likes']
    )


# change the logic

@router.post('/')
async def like(response: schemas.Likes, db: Session = Depends(database.get_db), current_user: int = Depends(outh.get_current_user)):
    
    exist = db.query(models.Likes).filter(models.Likes.user_id == current_user.id, models.Likes.note_id == response.note_id).first()
    
    if exist:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail='Already responded')
    
    # note_query = db.query(models.Notes).filter(models.Notes.id == response.note_id)
    
    new_response = models.Likes(user_id = current_user.id, **response.model_dump())
    db.add(new_response)
    db.commit()
    db.refresh()
    
    return 'Succesfully Added vote'