from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Optional
from wtforms.widgets import TextArea
from app.constants import notetype as NOTE_CONSTANTS

class NoteForm(FlaskForm):
    type = SelectField('Note Type', choices=[
                                        ('', ''),
                                        (str(NOTE_CONSTANTS.GENERAL), 'General'),
                                        (str(NOTE_CONSTANTS.CALL_LOG), 'Log Call')],
                            validators=[DataRequired()])
    comments = StringField('Comments', validators=[DataRequired()], widget=TextArea())
