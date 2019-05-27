from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired
from app.constants import dataset as DATASET_CONSTANTS

class UploadForm(FlaskForm):
    file = FileField(validators=[
        FileRequired(),
        FileAllowed(['xls', 'xlsx', 'csv'], 'CSV/Excel only!')
    ])

class DatasetUploadForm(UploadForm):
    provider = SelectField('Provider Type', choices=[
                                        ('', ''),
                                        (str(DATASET_CONSTANTS.UNKNOWN), 'Unknown'),
                                        (str(DATASET_CONSTANTS.ZILLOW), 'Zillow'),
                                        (str(DATASET_CONSTANTS.HUD), 'HUD')],
                            validators=[DataRequired()])
    dataset_type = SelectField('Dataset Type', choices=[
                                        ('', ''),
                                        (str(DATASET_CONSTANTS.FMR), 'Fair Market Rents'),
                                        (str(DATASET_CONSTANTS.MEDIAN_RENT_LIST_PRICE_3BR), '3BR Median Rents'),
                                        (str(DATASET_CONSTANTS.PRICE_TO_RENT_RATIO), 'Price To Rent Ratio'),
                                        (str(DATASET_CONSTANTS.MEDIAN_RENT_LIST_PRICE_NON_MULTI), 'Median Rent List Price ($), SFR, Condo/Co-op')],
                            validators=[DataRequired()])
    region_type = SelectField('Region Type', choices=[
                                        ('', ''),
                                        (str(DATASET_CONSTANTS.METRO_US), 'Metro & U.S.'),
                                        (str(DATASET_CONSTANTS.STATE), 'State'),
                                        (str(DATASET_CONSTANTS.COUNTY), 'County'),
                                        (str(DATASET_CONSTANTS.CITY), 'City'),
                                        (str(DATASET_CONSTANTS.ZIP_CODE), 'Zip Code'),
                                        (str(DATASET_CONSTANTS.NEIGHBORHOOD), 'Neighborhood'),
                                        ],
                            validators=[DataRequired()])
