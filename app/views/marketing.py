from flask import g, render_template, flash, redirect, url_for, request
from app import db
from app.views import marketing_bp as bp
from app.forms.search import SearchForm
from flask_security import current_user
from app.models.contact import Contact
from app.models.property import PropertyContact

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

@bp.route('/leads')
def leads():
    leads = current_user.get_contact_leads()
    return render_template('marketing/leads/all.html',
                            title="Leads",
                            leads=leads)

@bp.route('/leads/<lead_id>')
def lead(lead_id):
    lead = Contact.query.get(lead_id)
    property_contacts = PropertyContact.query.filter_by(contact_id=lead.id)
    properties = [contact.property for contact in property_contacts if contact.role == "Owner"]
    return render_template('marketing/leads/view.html',
                            title="View",
                            lead=lead,
                            properties=properties)
