from sqlalchemy import func
from app.crm.models import Contact

def search_for_contacts(user, first_name, last_name):
    query = Contact.query.filter_by(create_user_id=user.id)
    if first_name is not None and first_name is not "":
        query = query.filter(func.lower(Contact.first_name).like('%' + func.lower(first_name) + '%'))
    if last_name is not None and last_name is not "":
        query = query.filter(func.lower(Contact.last_name).like('%' + func.lower(last_name) + '%'))
    return query.all()
