from flask import g, render_template, flash, redirect, url_for, request
from app import db
from app.views import proformas_bp as bp
from app.forms.search import SearchForm
from flask_security import current_user
from app.models.property import Property
from app.models.proforma import *
from app.forms.proforma import *

@bp.before_app_request
def before_request():
    g.search_form = SearchForm()

@bp.route('/<proforma_id>')
def view(proforma_id):
    proforma = Proforma.query.get(proforma_id)
    form = ProformaForm(obj=proforma)
    return render_template('proformas/view.html',
                            title="View",
                            proforma=proforma,
                            form=form)

@bp.route('/add/<property_id>', methods=['GET', 'POST'])
def create(property_id):
    property = Property.query.get(property_id)
    form = ProformaForm()
    if form.validate_on_submit():
        proforma = Proforma()
        form.populate_obj(proforma)
        property.addProforma(proforma)
        db.session.add(property)
        db.session.commit()
        return redirect(url_for('deals.view', property_id=property_id))
    return render_template('proformas/create.html',
                            title="Add Proforma",
                            property=property,
                            form=form)

@bp.route('/delete/<proforma_id>', methods=['GET', 'POST'])
def delete(proforma_id):
     proforma = Proforma.query.get(proforma_id)
     property = proforma.property
     db.session.delete(proforma)
     db.session.commit()
     return redirect(url_for('deals.view', property_id=property.id))

@bp.route('<proforma_id>/add/income', methods=['GET', 'POST'])
def add_income(proforma_id):
    proforma = Proforma.query.get(proforma_id)
    form = LineItemForm()
    if form.validate_on_submit():
        line_item = LineItem()
        form.populate_obj(line_item)
        proforma.addIncomeLineItem(line_item)
        db.session.add(proforma)
        db.session.commit()
        return redirect(url_for('proformas.view', proforma_id=proforma.id))
    return render_template('proformas/line_item.html',
                            title="Add Proforma",
                            line_item_type="Income",
                            proforma=proforma,
                            form=form)

@bp.route('<proforma_id>/add/expense', methods=['GET', 'POST'])
def add_expense(proforma_id):
    proforma = Proforma.query.get(proforma_id)
    form = LineItemForm()
    if form.validate_on_submit():
        line_item = LineItem()
        form.populate_obj(line_item)
        proforma.addExpenseLineItem(line_item)
        db.session.add(proforma)
        db.session.commit()
        return redirect(url_for('proformas.view', proforma_id=proforma.id))
    return render_template('proformas/line_item.html',
                            title="Add Proforma",
                            line_item_type="Income",
                            proforma=proforma,
                            form=form)
