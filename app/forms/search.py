from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional
from app.constants import propertytype as PROPERTY_CONSTANTS

class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

class PropertySearchForm(FlaskForm):
    property_type = SelectField('Property Type', choices=[
                                        ('', ''),
                                        (str(PROPERTY_CONSTANTS.OTHER), 'Other'),
                                        (str(PROPERTY_CONSTANTS.SFR), 'Single Family'),
                                        (str(PROPERTY_CONSTANTS.RESIDENTIAL_MULTI_FAMILY), 'Residential Multi Family'),
                                        (str(PROPERTY_CONSTANTS.COMMERCIAL_MULTI_FAMILY), 'Commercial Multi Fmaily'),
                                        (str(PROPERTY_CONSTANTS.SELF_STORAGE), 'Self Storage'),
                                        (str(PROPERTY_CONSTANTS.RETAIL), 'Retail')],
                            validators=[Optional()])
    bedrooms = IntegerField('Bedrooms', validators=[Optional()])
    bathrooms = IntegerField('Bathrooms', validators=[Optional()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(PropertySearchForm, self).__init__(*args, **kwargs)
