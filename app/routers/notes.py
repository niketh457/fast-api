from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, APIRouter
from .. import models
from ..database import get_db
from app.schemas import NoteResponse, NoteBase
from ..outh import get_current_user

router = APIRouter(
    prefix='/notes',
    tags=['Notes']
)


@router.get("/", response_model=List[NoteResponse])
async def get_notes(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 10, search: Optional[str] = ''):
    # cursor.execute('''SELECT * FROM "Notes"''')
    # notes = cursor.fetchall()

    notes = db.query(models.Notes).limit(limit).all()
    
    return notes


@router.post('/', status_code=status.HTTP_201_CREATED, response_model = NoteResponse)
def post(req: NoteBase, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute("""INSERT INTO "Notes" (note, important) VALUES (%s, %s) RETURNING *""", (req.note, req.important))
    # #  RETURNING * returns the executed query (If it is not provided the data will not be returned by api)
    # new_note = cursor.fetchone()  # returned data will be stored in this variable
    # conn.commit()  # Now the data will be stored in the postgres

    # new_note = models.Notes(title=req.title, note=req.note, completed=req.completed)
    # The above can also be written as...
    new_note = models.Notes(user_id = current_user.id, **req.model_dump())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get('/{id}', response_model=NoteResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):  # it will be validated by fastapi itself
    # cursor.execute("""SELECT * FROM "Notes" WHERE id = (%s)""", vars=(str(id), ))  # by using %s it should be
    # string if, is not present after the str(id) then not all the integers will be converted to str
    #
    # req_note = cursor.fetchone()
    #
    # if not req_note:
    #     # response.status_code = 404
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {'detail': f'note with id {id} not found'}
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'note with id {id} not found')

    req_note = db.query(models.Notes).filter(models.Notes.id == id, models.Notes.user_id == current_user.id).first()

    if not req_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Note with id {id} not found')

    return req_note


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    # cursor.execute("""DELETE FROM "Notes" WHERE id = (%s) RETURNING *""", (str(id),))
    # deleted_note = cursor.fetchone()
    # conn.commit()  # don't forget to commit changes if something is altered in database
    # if not deleted_note:
    #     # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'note with id {id} not found')
    #     return Response(status_code=status.HTTP_204_NO_CONTENT)

    query = db.query(models.Notes).filter(models.Notes.user_id == current_user.id, models.Notes.id == id)
    deleted_note = query.first()

    if deleted_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'note with id {id} not found for the user with user_id {current_user.id}')

    query.delete(synchronize_session=False)  # just remember as thumb rule
    db.commit()
    # db.refresh(deleted_note)

# nothing should be returned when delete operation is done except the status code


@router.put('/{id}', response_model=NoteResponse)
def update_note(id: int, updated_note: NoteBase, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute("""UPDATE "Notes" SET NOTE = %s, IMPORTANT = %s WHERE ID = %s RETURNING *""",
    # (updated_note.note, updated_note.important, str(id), )) new_note = cursor.fetchone() conn.commit() if not
    # new_note: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'note with id {id} not found')

    sql = db.query(models.Notes).filter(models.Notes.id == id, models.Notes.user_id == current_user.id)

    new_note = sql.first()

    if not new_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Note with id {id} not found')

    sql.update(updated_note.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(new_note)

    return new_note
