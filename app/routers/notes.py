from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, APIRouter

from .. import models
from ..database import get_db

from app.schemas import NoteResponse, NoteBase

note_route = APIRouter()


@note_route.get("/notes", response_model=List[NoteResponse])
async def get_notes(db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM "Notes"''')
    # notes = cursor.fetchall()

    notes = db.query(models.Notes).all()
    return notes


@note_route.post('/notes', status_code=status.HTTP_201_CREATED, response_model=NoteResponse)
def post(req: NoteBase, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO "Notes" (note, important) VALUES (%s, %s) RETURNING *""", (req.note, req.important))
    # #  RETURNING * returns the executed query (If it is not provided the data will not be returned by api)
    # new_note = cursor.fetchone()  # returned data will be stored in this variable
    # conn.commit()  # Now the data will be stored in the postgres

    # new_note = models.Notes(title=req.title, note=req.note, completed=req.completed)
    # The above can also be written as...
    new_note = models.Notes(**req.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@note_route.get('/notes/{id}', response_model=NoteResponse)
def get_post(id: int, db: Session = Depends(get_db)):  # it will be validated by fastapi itself
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

    req_note = db.query(models.Notes).filter(models.Notes.id == id).first()

    if not req_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Note with id {id} not found')

    return req_note


@note_route.delete('/notes/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int, db: Session = Depends(get_db)):
    #
    # cursor.execute("""DELETE FROM "Notes" WHERE id = (%s) RETURNING *""", (str(id),))
    # deleted_note = cursor.fetchone()
    # conn.commit()  # don't forget to commit changes if something is altered in database
    # if not deleted_note:
    #     # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'note with id {id} not found')
    #     return Response(status_code=status.HTTP_204_NO_CONTENT)

    deleted_note = db.query(models.Notes).filter(models.Notes.id == id)

    if not deleted_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'note with id {id} not found')

    deleted_note.delete(synchronize_session=False)  # just remember as thumb rule
    db.commit()
    # db.refresh(deleted_note)

    return deleted_note


# nothing should be returned when delete operation is done except the status code


@note_route.put('/notes/{id}', response_model=NoteResponse)
def update_note(id: int, updated_note: NoteBase, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE "Notes" SET NOTE = %s, IMPORTANT = %s WHERE ID = %s RETURNING *""",
    # (updated_note.note, updated_note.important, str(id), )) new_note = cursor.fetchone() conn.commit() if not
    # new_note: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'note with id {id} not found')

    sql = db.query(models.Notes).filter(models.Notes.id == id)

    new_note = sql.first()

    if not new_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Note with id {id} not found')

    sql.update(updated_note.dict(), synchronize_session=False)

    db.commit()
    db.refresh(new_note)

    return new_note
