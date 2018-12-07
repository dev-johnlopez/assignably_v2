from app import db
from app import constants as CONSTANTS
from app.mixins.audit import AuditMixin

class Property(db.Model, AuditMixin):
    __tablename__ = 'property'
    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    address = db.relationship('Address', uselist=False)
    contacts = db.relationship("PropertyContact")
    property_type = db.Column(db.Integer)
    units = db.Column(db.Integer, default=1)
    sq_feet = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    basement_type = db.Column(db.String(255))
    garage_type = db.Column(db.String(255))
    last_sale_date = db.Column(db.Date)
    owner_occupied = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.OTHER,
        'polymorphic_on':property_type
    }

    def __repr__(self):
        return str(self.address)

    def getPropertyType(self):
          return CONSTANTS.PROPERTY_TYPE[self.property_type]

    def addOwner(self, contact):
        if contact is not None:
            self.contacts.append(PropertyContact(contact=contact, role="Owner"))

    def addOwners(self, owners):
        for owner in owners:
            self.addOwner(owner)

class ResidentialProperty(Property):

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.RESIDENTIAL
    }

    def __init__(self, **kwargs):
        super(ResidentialProperty, self).__init__(**kwargs)


class SingleFamilyProperty(ResidentialProperty):

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.SFR
    }

    def __init__(self, **kwargs):
        super(SingleFamilyProperty, self).__init__(**kwargs)

class ResidentialMultiFamilyProperty(ResidentialProperty):

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.RESIDENTIAL_MULTI_FAMILY
    }

    def __init__(self, **kwargs):
        super(ResidentialMultiFamilyProperty, self).__init__(**kwargs)

class CommercialProperty(Property):

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.COMMERCIAL
    }

    def __init__(self, **kwargs):
        super(CommercialProperty, self).__init__(**kwargs)

class CommercialMultiFamilyProperty(CommercialProperty):

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.COMMERCIAL_MULTI_FAMILY
    }

    def __init__(self, **kwargs):
        super(CommercialMultiFamilyProperty, self).__init__(**kwargs)

class SelfStorageProperty(CommercialProperty):

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.SELF_STORAGE
    }

    def __init__(self, **kwargs):
        super(SelfStorageProperty, self).__init__(**kwargs)

class RetailProperty(CommercialProperty):

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.RETAIL
    }

    def __init__(self, **kwargs):
        super(RetailProperty, self).__init__(**kwargs)

class PropertyContact(db.Model, AuditMixin):
    __tablename__ = "property_contact"
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    property = db.relationship("Property", back_populates="contacts")
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship("Contact")
    role = db.Column(db.String(255))
