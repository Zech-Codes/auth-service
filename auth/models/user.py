from __future__ import annotations
from auth.database import Database
from auth.models import BaseModel
from typing import AnyStr, Optional
import sqlalchemy


class User(BaseModel):
    __tablename__ = 'Users'

    ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)

    @classmethod
    def get_user(cls, username: AnyStr, db: Optional[Database] = None) -> Optional[User]:
        with Database.get_connection(db) as session:
            return session.query(cls).filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email: AnyStr, db: Optional[Database] = None) -> Optional[User]:
        with Database.get_connection(db) as session:
            return session.query(cls).filter_by(email=email).first()

    @classmethod
    def get_user_by_id(cls, user_id: int, db: Optional[Database] = None) -> Optional[User]:
        with Database.get_connection(db) as session:
            return session.query(cls).filter_by(ID=user_id).first()

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}', email='{self.email}')>"
