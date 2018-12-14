from app import create_app, db
from app.models.role import Role
from app.models.user import User, Notification
from app.models.address import Address
from app.models.contact import Contact
from app.models.property import Property, PropertyContact, PropertyContactRole

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': User,
            'Role': Role,
            'Address' : Address,
            'Contact': Contact,
            'Notification': Notification,
            'Property': Property,
            'PropertyContact': PropertyContact,
            'PropertyContactRole': PropertyContactRole}
