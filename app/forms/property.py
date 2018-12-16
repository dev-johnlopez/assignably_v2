from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FormField, BooleanField, TextAreaField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import TextArea
from app.forms.address import AddressForm
from app.constants import propertytype as PROPERTY_CONSTANTS
from app.models.address import Address

class PropertyForm(FlaskForm):
    address = FormField(AddressForm, default=lambda: Address())
    owner_occupied = BooleanField()
    units = IntegerField('# Units', validators=[DataRequired()])
    property_type = SelectField('Property Type', choices=[
                                        ('', ''),
                                        (str(PROPERTY_CONSTANTS.OTHER), 'Other'),
                                        (str(PROPERTY_CONSTANTS.SFR), 'Single Family'),
                                        (str(PROPERTY_CONSTANTS.RESIDENTIAL_MULTI_FAMILY), 'Residential Multi Family'),
                                        (str(PROPERTY_CONSTANTS.COMMERCIAL_MULTI_FAMILY), 'Commercial Multi Fmaily'),
                                        (str(PROPERTY_CONSTANTS.SELF_STORAGE), 'Self Storage'),
                                        (str(PROPERTY_CONSTANTS.RETAIL), 'Retail')],
                            validators=[DataRequired()])
    units = IntegerField('# Units', validators=[Optional()])
    sq_feet = IntegerField('Sq. Feet', validators=[Optional()])
    bedrooms = IntegerField('Bedrooms', validators=[Optional()])
    bathrooms = IntegerField('Bathrooms', validators=[Optional()])
    basement_desc = StringField('Basement Description', validators=[Optional()], widget=TextArea())
    garage_desc = StringField('Garage Description', validators=[Optional()], widget=TextArea())
    last_sale_date = DateField('Last Sale Date', validators=[Optional()])
    owner_occupied = BooleanField('Owner Occupied?', validators=[Optional()])
