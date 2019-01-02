from flask import g, render_template, flash, redirect, url_for, request
from app import db
from app.views import deals_bp as bp
from app.forms.search import SearchForm
from flask_security import current_user
from app.models.property import PropertyContact, Property
from app.forms.property import PropertyForm
from app.forms.proforma import ProformaForm
from app.forms.search import PropertySearchForm

@bp.before_app_request
def before_request():
    g.search_form = SearchForm()

@bp.route('/all', methods=['GET'])
def all():
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
    return render_template('deals/all.html',
                            title="View",
                            form=form,
                            properties=properties)


@bp.route('/<property_id>')
def view(property_id):
    property = Property.query.get(property_id)
    return render_template('deals/view.html',
                            title="View",
                            property=property)

@bp.route('/<property_id>/edit', methods=['GET', 'POST'])
def edit(property_id):
    property = Property.query.get(property_id)
    form = PropertyForm(obj=property)
    if form.validate_on_submit():
        form.populate_obj(property)
        db.session.add(property)
        db.session.commit()
        return redirect(url_for('deals.view', property_id=property_id))
    return render_template('deals/edit.html',
                            title="Edit",
                            property=property,
                            form=form)

@bp.route('/<property_id>/profroma/add', methods=['GET', 'POST'])
def add_proforma(property_id):
    property = Property.query.get(property_id)
    form = ProformaForm()
    if form.validate_on_submit():
        return redirect(url_for('deals.view', property_id=property_id))
    return render_template('deals/proforma.html',
                            title="Add Proforma",
                            property=property,
                            form=form)
