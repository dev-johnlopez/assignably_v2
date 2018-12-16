from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Optional

class LeadForm(FlaskForm):
    first_name = StringField('First Name', validators=[])
    last_name = StringField('Last Name', validators=[])
    phone = StringField('Phone', validators=[])
    email = StringField('Email', validators=[Optional(), Email()])
