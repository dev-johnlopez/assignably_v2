from flask import g, render_template, flash, redirect, url_for, request
from app import db
from app.views import proformas_bp as bp
from app.forms.search import SearchForm
from flask_security import current_user
from app.models.property import Property
from app.models.proforma import *
from app.forms.proforma import *
import locale

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

@bp.route('/<proforma_id>/cashflow')
def cashflow(proforma_id):
    proforma = Proforma.query.get(proforma_id)
    return render_template('proformas/cashflow.html',
                            title="Cashflow Analysis",
                            proforma=proforma)

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

@bp.route('edit/income/<line_item_id>', methods=['GET', 'POST'])
def edit_income(line_item_id):
    line_item = LineItem.query.get(line_item_id)
    proforma = Proforma.query.get(line_item.income_proforma_id)
    form = LineItemForm(obj=line_item_type)
    if form.validate_on_submit():
        form.populate_obj(line_item)
        db.session.add(line_item)
        db.session.commit()
        return redirect(url_for('proformas.view', proforma_id=proforma.id))
    return render_template('proformas/line_item.html',
                            title="Edit Proforma",
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
                            line_item_type="Expense",
                            proforma=proforma,
                            form=form)

@bp.route('edit/expense/<line_item_id>', methods=['GET', 'POST'])
def edit_expense(line_item_id):
    line_item = LineItem.query.get(line_item_id)
    proforma = Proforma.query.get(line_item.expense_proforma_id)
    form = LineItemForm(obj=line_item)
    if form.validate_on_submit():
        form.populate_obj(line_item)
        db.session.add(line_item)
        db.session.commit()
        return redirect(url_for('proformas.view', proforma_id=proforma.id))
    return render_template('proformas/line_item.html',
                            title="Edit Expense",
                            line_item_type="Expense",
                            proforma=proforma,
                            form=form)

@bp.route('/delete/line_item/<line_item_id>', methods=['GET', 'POST'])
def delete_line_item(line_item_id):
     line_item = LineItem.query.get(line_item_id)
     proforma = line_item.proforma
     db.session.delete(line_item)
     db.session.commit()
     return redirect(url_for('proformas.view', proforma_id=proforma.id))

@bp.route('<proforma_id>/add/loan', methods=['GET', 'POST'])
def add_loan(proforma_id):
    proforma = Proforma.query.get(proforma_id)
    form = LoanForm()
    if form.validate_on_submit():
        loan = Loan()
        form.populate_obj(loan)
        proforma.addLoan(loan)
        db.session.add(proforma)
        db.session.commit()
        return redirect(url_for('proformas.view', proforma_id=proforma.id))
    return render_template('proformas/financing.html',
                            title="Add Loan",
                            proforma=proforma,
                            form=form)

@bp.route('edit/loan/<loan_id>', methods=['GET', 'POST'])
def edit_loan(loan_id):
    loan = Loan.query.get(loan_id)
    proforma = loan.proforma
    form = LoanForm(obj=loan)
    if form.validate_on_submit():
        form.populate_obj(loan)
        db.session.add(loan)
        db.session.commit()
        return redirect(url_for('proformas.view', proforma_id=proforma.id))
    return render_template('proformas/financing.html',
                            title="Edit Loan",
                            proforma=proforma,
                            form=form)

@bp.route('/delete/loan/<loan_id>', methods=['GET', 'POST'])
def delete_loan(loan_id):
     loan = Loan.query.get(loan_id)
     proforma = Proforma.query.get(loan.proforma_id)
     db.session.delete(loan)
     db.session.commit()
     return redirect(url_for('proformas.view', proforma_id=proforma.id))

@bp.app_template_filter()
def currency(value):
    return locale.currency(value, grouping=True )