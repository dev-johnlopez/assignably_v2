from app import db
from app.mixins.audit import AuditMixin
from app.constants import proforma as PROFORMA_CONSTANTS

class Proforma(db.Model, AuditMixin):
    __tablename__ = "proforma"
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    property = db.relationship("Property", back_populates="proformas")
    arv = db.Column(db.Integer)
    purchase_price = db.Column(db.Integer)
    seller_concessions = db.Column(db.Integer)
    closing_costs = db.Column(db.Integer)
    rent_ready_costs = db.Column(db.Integer)
    initial_reserve_amount = db.Column(db.Integer)
    lease_option_fee = db.Column(db.Integer)
    total_finished_sq_foot = db.Column(db.Integer)
    land_value_perc = db.Column(db.Numeric(precision=5,scale=2))
    income_tax_rate = db.Column(db.Numeric(precision=5,scale=2))
    vacancy_perc = db.Column(db.Numeric(precision=5,scale=2))
    loans = db.relationship('Loan')
    income = db.relationship('LineItem', foreign_keys="[LineItem.income_proforma_id]")
    expenses = db.relationship('LineItem', foreign_keys="[LineItem.expense_proforma_id]")

    def addIncomeLineItem(self, line_item):
        if self.income is None:
            self.income = []
        self.income.append(line_item)

    def addExpenseLineItem(self, line_item):
        if self.expenses is None:
            self.expenses = []
        self.expenses.append(line_item)


class Loan(db.Model, AuditMixin):
    __tablename__ = "loan"
    id = db.Column(db.Integer, primary_key=True)
    proforma_id = db.Column(db.Integer, db.ForeignKey('proforma.id'))
    type = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    interest_rate = db.Column(db.Numeric(precision=6,scale=3))
    interest_only = db.Column(db.Boolean)
    length = db.Column(db.Integer)

class LineItem(db.Model, AuditMixin):
    __tablename__ = "line_item"
    id = db.Column(db.Integer, primary_key=True)
    income_proforma_id = db.Column(db.Integer, db.ForeignKey('proforma.id'))
    expense_proforma_id = db.Column(db.Integer, db.ForeignKey('proforma.id'))
    type = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    frequency = db.Column(db.Integer)
    annual_increase_perc = db.Column(db.Numeric(precision=6,scale=2))

    def getFrequency(self):
        return PROFORMA_CONSTANTS.FREQUENCY_TYPE[self.frequency]
