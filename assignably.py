from app import create_app, db
from app.models.role import Role
from app.models.user import User
from app.models.address import Address
from app.models.contact import Contact

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': User,
            'Role': Role,
            'Address' : Address,
            'Contact': Contact}
