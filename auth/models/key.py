from ..models import BaseModel
import sqlalchemy


class Key(BaseModel):
    __tablename__ = 'Users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    key = sqlalchemy.Column(sqlalchemy.String)
    generated = sqlalchemy.Column(sqlalchemy.DateTime)

    def __repr__(self):
        return f"<Key(id='{self.id}', name='{self.name}' key='{self.key}', generated='{self.generated}')>"
