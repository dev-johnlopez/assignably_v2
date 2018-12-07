from app import db
from app.mixins.audit import AuditMixin
from app.mixins.searchable import SearchableMixin
from app.models.property import Property, PropertyContact


class Contact(db.Model, AuditMixin, SearchableMixin):
    __tablename__ = 'contact'
    __searchable__ = ['first_name', 'last_name', 'phone']
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    contact_type = db.Column(db.String(50))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255))
    mailing_address = db.relationship('Address', uselist=False)
    mailing_address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

    __mapper_args__ = {
        'polymorphic_identity':'contact',
        'polymorphic_on':contact_type
    }

    def __init__(self, **kwargs):
        self.addresses = []
        super(Contact, self).__init__(**kwargs)

    def __repr__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def setMailingAddress(self, address):
        self.mailing_address = address
        #if hasProperty(address):

    def getProperty(self, address):
        return Property.query.join(Address).filter(Address.id==address.id)

    def getProperties(self):
        return Property.query.join(PropertyContact).filter(PropertyContact.contact_id == self.id)

    def getNumberOfProperties(self):
        return Property.query.join(PropertyContact).filter(PropertyContact.contact_id == self.id).count()


class Investor(Contact):
    #investment_strategy = db.Column(db.String(255))
    #investment_criteria = db.relationship('InvestmentCriteria')
    #notes = db.Column(db.String(2500))

    __mapper_args__ = {
        'polymorphic_identity':'investor'
    }

class Lead(Contact):

    __mapper_args__ = {
        'polymorphic_identity':'lead'
    }
