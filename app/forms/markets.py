from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired, Email, Optional
from wtforms.widgets import TextArea
from app.constants import dataset as DATASET_CONSTANTS

class RegionForm(FlaskForm):
    region_type = SelectField('Region Type', choices=[
                                        ('', ''),
                                        (str(DATASET_CONSTANTS.METRO_US), 'Metro & US'),
                                        (str(DATASET_CONSTANTS.STATE), 'State'),
                                        (str(DATASET_CONSTANTS.COUNTY), 'County'),
                                        (str(DATASET_CONSTANTS.CITY), 'City'),
                                        (str(DATASET_CONSTANTS.ZIP_CODE), 'Zip Code'),
                                        (str(DATASET_CONSTANTS.NEIGHBORHOOD), 'Neighborhood')],
                            validators=[DataRequired()])
    region_id = SelectField('Region Type', choices=[],
                            validators=[DataRequired()])
