from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Notes(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    note = Column(String, nullable=False)
    completed = Column(Boolean, server_default='TRUE')
    noted_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer,
                     ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                     nullable=False)
    
    user = relationship('User')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Likes(Base):
    __tablename__ = 'likes'
    
    note_id = Column(Integer, ForeignKey('notes.id', ondelete='CASCADE'), primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key = True)
    like = Column(Boolean)


