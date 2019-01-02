from flask import g, render_template, flash, redirect, url_for, request
from app import db
from app.views import marketing_bp as bp
from app.forms.search import SearchForm
from flask_security import current_user
from app.models.contact import Contact
from app.models.note import Note
from app.models.property import PropertyContact, Property
from app.forms.lead import LeadForm
from app.forms.note import NoteForm
from app.forms.property import PropertyForm
from app.forms.search import PropertySearchForm
from app.constants import notetype as NOTE_CONSTANTS

@bp.before_app_request
def before_request():
    g.search_form = SearchForm()

@bp.route('/')
def index():
    contact_leads = current_user.get_contact_leads()
    property_leads = current_user.get_property_leads()
    return render_template('marketing/index.html',
                title='Dashboard',
                contact_leads=len(contact_leads),
                property_leads=len(property_leads))
