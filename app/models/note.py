from app import db
from app.mixins.audit import AuditMixin


class Note(db.Model, AuditMixin):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, default=True)
    comments = db.Column(db.String(5000))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'),
        nullable=True)
    contact = db.relationship('Contact', back_populates='notes')

    def __init__(self, **kwargs):
        super(Note, self).__init__(**kwargs)

    def getRelatedTo(self):
        if self.contact is not None:
            return self.contact
