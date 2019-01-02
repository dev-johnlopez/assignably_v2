from flask import g, render_template, flash, redirect, url_for, request
from app import db
from app.views import leads_bp as bp
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
def all():
    leads = current_user.get_contact_leads()
    return render_template('leads/all.html',
                            title="Leads",
                            leads=leads)

@bp.route('/leads/<lead_id>')
def view(lead_id):
    lead = Contact.query.get(lead_id)
    property_contacts = PropertyContact.query.filter_by(contact_id=lead.id)
    return render_template('leads/view.html',
                            title="View",
                            lead=lead,
                            property_contact_roles=property_contacts)

@bp.route('/leads/<lead_id>/edit', methods=['GET','POST'])
def edit(lead_id):
    lead = Contact.query.get(lead_id)
    form = LeadForm(obj=lead)
    if form.validate_on_submit():
        form.populate_obj(lead)
        db.session.add(lead)
        db.session.commit()
    return render_template('leads/edit.html',
                            title="Edit",
                            lead=lead,
                            form=form)

@bp.route('/leads/<lead_id>/add_note', methods=['GET','POST'])
def add_note(lead_id):
    lead = Contact.query.get(lead_id)
    form = NoteForm()
    if form.validate_on_submit():
        note = Note()
        form.populate_obj(note)
        lead.addNote(note)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('marketing.lead', lead_id=lead_id))
    return render_template('leads/log_call.html',
                            title="Edit",
                            lead=lead,
                            form=form)
