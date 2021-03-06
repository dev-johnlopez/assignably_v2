from app import db
from app.constants import propertytype as PROPERTY_CONSTANTS
from app.constants import contactrole as CONTACT_ROLE_CONSTANTS
from app.mixins.audit import AuditMixin
from app.src.util.factory.proforma_factory import ProformaFactory
from sqlalchemy import event

class Property(db.Model, AuditMixin):
    __tablename__ = 'property'
    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    address = db.relationship('Address', uselist=False)
    contacts = db.relationship("PropertyContact")
    property_type = db.Column(db.Integer)
    property_tax = db.Column(db.Integer)
    units = db.Column(db.Integer, default=1)
    sq_feet = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    basement_desc = db.Column(db.String(255))
    garage_desc = db.Column(db.String(255))
    last_sale_date = db.Column(db.Date)
    owner_occupied = db.Column(db.Boolean)
    proformas = db.relationship('Proforma', back_populates="property")

    __mapper_args__ = {
        'polymorphic_identity':PROPERTY_CONSTANTS.OTHER,
        'polymorphic_on':property_type
    }

    def __repr__(self):
        return str(self.address)

    def getPropertyType(self):
          return PROPERTY_CONSTANTS.PROPERTY_TYPE[self.property_type]

    def addOwner(self, contact):
        if contact is not None:
            if not self.hasContactWithRole(contact, int(CONTACT_ROLE_CONSTANTS.OWNER)):
                self.contacts.append(PropertyContact(contact=contact, roles=[PropertyContactRole(type=int(CONTACT_ROLE_CONSTANTS.OWNER))]))

    def addOwners(self, owners):
        for owner in owners:
            self.addOwner(owner)

    def hasContactWithRole(self, contact, role_code):
        for property_contact in self.contacts:
            if property_contact.hasRole(role_code) and property_contact.contact == contact:
                return True
        return False

    def addProforma(self, proforma):
        if self.proformas is None:
            self.proformas = []
        self.proformas.append(proforma)

    def canAutoEvaluate(self):
        return self.bedrooms is not None and self.property_tax is not None

class ResidentialProperty(Property):

    __mapper_args__ = {
        'polymorphic_identity':PROPERTY_CONSTANTS.RESIDENTIAL
    }

    def __init__(self, **kwargs):
        super(ResidentialProperty, self).__init__(**kwargs)


class SingleFamilyProperty(ResidentialProperty):

    __mapper_args__ = {
        'polymorphic_identity':PROPERTY_CONSTANTS.SFR
    }

    def __init__(self, **kwargs):
        super(SingleFamilyProperty, self).__init__(**kwargs)

class ResidentialMultiFamilyProperty(ResidentialProperty):

    __mapper_args__ = {
        'polymorphic_identity':PROPERTY_CONSTANTS.RESIDENTIAL_MULTI_FAMILY
    }

    def __init__(self, **kwargs):
        super(ResidentialMultiFamilyProperty, self).__init__(**kwargs)

class CommercialProperty(Property):

    __mapper_args__ = {
        'polymorphic_identity':PROPERTY_CONSTANTS.COMMERCIAL
    }

    def __init__(self, **kwargs):
        super(CommercialProperty, self).__init__(**kwargs)

class CommercialMultiFamilyProperty(CommercialProperty):

    __mapper_args__ = {
        'polymorphic_identity':PROPERTY_CONSTANTS.COMMERCIAL_MULTI_FAMILY
    }

    def __init__(self, **kwargs):
        super(CommercialMultiFamilyProperty, self).__init__(**kwargs)

class SelfStorageProperty(CommercialProperty):

    __mapper_args__ = {
        'polymorphic_identity':PROPERTY_CONSTANTS.SELF_STORAGE
    }

    def __init__(self, **kwargs):
        super(SelfStorageProperty, self).__init__(**kwargs)

class RetailProperty(CommercialProperty):

    __mapper_args__ = {
        'polymorphic_identity':PROPERTY_CONSTANTS.RETAIL
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
    roles = db.relationship("PropertyContactRole")

    def addOwnerRole(self):
        role = PropertyContactRole(type=int(CONTACT_ROLE_CONSTANTS.OWNER))
        self.addRole(role)
        db.session.add(role)

    def addRole(self):
        if self.roles is None:
            self.roles = []
        self.roles.append(role)

    def hasRole(self, role_code):
        for role in self.roles:
            if role.type == role_code:
                return True
        return False

    def getAllRoleNames(self):
        return ', '.join([str(role.getRoleType()) for role in self.roles])

class PropertyContactRole(db.Model, AuditMixin):
    __tablename__ = "property_contact_role"
    id = db.Column(db.Integer, primary_key=True)
    property_contact_id = db.Column(db.Integer, db.ForeignKey('property_contact.id'))
    type = db.Column(db.Integer)

    def getRoleType(self):
        return CONTACT_ROLE_CONSTANTS.CONTACT_ROLE[self.type]

def add_proformas(mapper, connection, target):
    if target.canAutoEvaluate():
        ProformaFactory.buildProfromasFromProperty(target)

event.listen(Property, 'after_insert', add_proformas)
event.listen(Property, 'after_update', add_proformas)
event.listen(SingleFamilyProperty, 'after_insert', add_proformas)
event.listen(SingleFamilyProperty, 'before_update', add_proformas)
