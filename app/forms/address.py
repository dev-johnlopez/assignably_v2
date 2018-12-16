from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FormField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class AddressForm(FlaskForm):
    line_1 = StringField('Street Address', validators=[])
    line_2 = StringField('Unit / Apt', validators=[])
    city = StringField('City', validators=[])
    state_code = SelectField('State', choices=[
        ('',''),
        ('AK','Alaska'),
        ('AL','Alabama'),
        ('AR','Arkansas'),
        ('AZ','Arizona'),
        ('CA','California'),
        ('CT','Connecticut'),
        ('DC','Washington DC'),
        ('DE','Delaware'),
        ('FL','Florida'),
        ('GA','Georgia'),
        ('HI','Hawaii'),
        ('IA','Iowa'),
        ('ID','Idaho'),
        ('IL','Illinois'),
        ('IN','Indiana'),
        ('KS','Kansas'),
        ('KY','Kentucky'),
        ('LA','Louisiana'),
        ('MA','Massachusetts'),
        ('MA','Massachusetts'),
        ('MD','Maryland'),
        ('ME','Maine'),
        ('MI','Michigan'),
        ('MN','Minnesota'),
        ('MO','Missouri'),
        ('MS','Mississippi'),
        ('MT','Montana'),
        ('NC','North Carolina'),
        ('ND','North Dakota'),
        ('NE','Nebraska'),
        ('NH','New Hampshire'),
        ('NJ','New Jersey'),
        ('NM','New Mexico'),
        ('NV','Nevada'),
        ('NY','New York'),
        ('OH','Ohio'),
        ('OK','Oklahoma'),
        ('OR','Oregon'),
        ('PA','Pennsylvania'),
        ('RI','Rhode Island'),
        ('SC','South Carolina'),
        ('SD','South Dakota'),
        ('TN','Tennessee'),
        ('TX','Texas'),
        ('UT','Utah'),
        ('VA','Virginia'),
        ('VT','Vermont'),
        ('WA','Washington'),
        ('WI','Wisconsin'),
        ('WV','West Virginia'),
        ('WY','Wyoming')
    ], validators=[])
    postal_code = StringField('ZIP Code', validators=[])
