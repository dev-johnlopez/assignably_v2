from app import db
from sqlalchemy.ext.declarative import declared_attr
from flask_security import current_user, AnonymousUser
from datetime import datetime
# Define a base model for other database tables to inherit
class BaseModel(db.Model):

    __abstract__  = True

    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    @declared_attr
    def create_user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self):
        super(BaseModel,self).__init__()
        if current_user.is_authenticated:
            self.create_user_id = current_user.id

    def delete(self):
        db.session.delete(self)
