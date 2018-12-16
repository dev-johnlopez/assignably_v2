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
    #properties = [contact.property for contact in property_contacts if contact.role == "Owner"]
    return render_template('marketing/leads/view.html',
                            title="View",
                            lead=lead,
                            property_contact_roles=property_contacts)

@bp.route('/leads/<lead_id>/edit', methods=['GET','POST'])
def edit_lead(lead_id):
    lead = Contact.query.get(lead_id)
    form = LeadForm(obj=lead)
    if form.validate_on_submit():
        form.populate_obj(lead)
        db.session.add(lead)
        db.session.commit()
    return render_template('marketing/leads/edit.html',
                            title="Edit",
                            lead=lead,
                            form=form)

@bp.route('/leads/<lead_id>/log_call', methods=['GET','POST'])
def log_call(lead_id):
    lead = Contact.query.get(lead_id)
    form = NoteForm()
    if form.validate_on_submit():
        note = Note()
        form.populate_obj(note)
        lead.addNote(note)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('marketing.lead', lead_id=lead_id))
    flash(form.errors, 'error')
    return render_template('marketing/leads/log_call.html',
                            title="Edit",
                            lead=lead,
                            form=form)

@bp.route('/properties', methods=['GET'])
def all_properties():
    properties = []
    form = PropertySearchForm()
    if form.validate():
        temp_properties = current_user.get_property_leads()
        bedroom_filter = None
        bathroom_filter = None
        property_type_filter = None
        if form.bedrooms.data is not None:
            bedroom_filter = int(form.bedrooms.data)
        if form.bathrooms.data is not None:
            bathroom_filter = int(form.bathrooms.data)
        if form.property_type.data is not None and form.property_type.data != 'None':
            property_type_filter = int(form.property_type.data)
        for property in temp_properties:
            if (bedroom_filter is None or property.bedrooms >= bedroom_filter) \
                and (bathroom_filter is None or property.bathrooms >= bathroom_filter) \
                and (property_type_filter is None or property.property_type == property_type_filter):
                properties.append(property)
    return render_template('marketing/properties/all.html',
                            title="View",
                            form=form,
                            properties=properties)


@bp.route('/properties/<property_id>')
def property(property_id):
    property = Property.query.get(property_id)
    return render_template('marketing/properties/view.html',
                            title="View",
                            property=property)

@bp.route('/properties/<property_id>/edit', methods=['GET', 'POST'])
def edit_property(property_id):
    property = Property.query.get(property_id)
    form = PropertyForm(obj=property)
    if form.validate_on_submit():
        form.populate_obj(property)
        db.session.add(property)
        db.session.commit()
        return redirect(url_for('marketing.property', property_id=property_id))
    return render_template('marketing/properties/edit.html',
                            title="Edit",
                            property=property,
                            form=form)
