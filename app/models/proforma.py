from app import db
from app.mixins.audit import AuditMixin
from app.constants import proforma as PROFORMA_CONSTANTS
from decimal import Decimal, ROUND_HALF_UP

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
    initial_reserve_amount = db.Column(db.Integer, default=0)
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

    def addLoan(self, loan):
        if self.loans is None:
            self.loans = []
        self.loans.append(loan)

    def getInvestedCash():
        return self.purchase_price  + self.closing_costs \
                + self.rent_ready_costs + self.initial_reserve_amount \
                - self.getTotalLoanAmount()- self.seller_concessions

    def getTotalLoanAmount(self):
        total_loan_amount = 0
        for loan in self.loans:
            total_loan_amount += loan.amount
        return total_loan_amount

    def getDebtService(self):
        debt_service_total = 0
        for loan in self.loans:
            debt_service_total += loan.getAnnualPayment()
        return debt_service_total

    def getGrossScheduledIncome(self):
        income_total = 0
        for line_item in self.income:
            income_total += line_item.getAnnualizedAmount()
        return income_total

    def getGrossScheduledIncomeByYear(self, year):
        income_total = 0
        for line_item in self.income:
            income_total += line_item.getCompoundingAmountByYear(year)
        return income_total

    def getGrossRentMultiplier(self):
        return self.arv / self.getGrossScheduledIncome()

    def getVacancyAndCreditLoss(self):
        return self.getGrossScheduledIncome() * self.vacancy_perc / 100

    def getVacancyAndCreditLossByYear(self, year):
        return self.getGrossScheduledIncomeByYear(year) * self.vacancy_perc / 100

    def getGrossOperatingIncome(self):
        return self.getGrossScheduledIncome() - self.getVacancyAndCreditLoss()

    def getGrossOperatingIncomeByYear(self, year):
        return self.getGrossScheduledIncomeByYear(year) - self.getVacancyAndCreditLossByYear(year)

    def getOperatingExpenses(self):
        expense_total = 0
        for line_item in self.expenses:
            expense_total += line_item.getAnnualizedAmount()
        return expense_total

    def getOperatingExpensesByYear(self, year):
        expense_total = 0
        for line_item in self.expenses:
            expense_total += line_item.getCompoundingAmountByYear(year)
        return expense_total

    def getNetOperatingIncome(self):
        return self.getGrossOperatingIncome() - self.getOperatingExpenses()

    def getCapitalizationRate(self):
        # TODO - Cap Rate should be based on aquisition costs not arv.
        return self.getNetOperatingIncome() / self.arv

    def getNetIncomeMultiplier(self):
        return 1 / self.getCapitalizationRate()

    def getPresentValue(self):
        return self.getNetIncomeMultiplier() * self.getNetOperatingIncome()

    def getTaxableIncome(self):
        #TODO - Net Operating Income less Mortgage Interest less Depreciation, Real property less Depreciation, Capital Additions less Amortization, Points and Closing Costs plus Interest Earned = Taxable Income
        return self.getNetOperatingIncome()

    def getCashflowBeforeTaxes(self):
        #TODO - Net Operating Income less Debt Service less Capital Additions plus Loan Proceeds plus Interest Earned
        return self.getNetOperatingIncome() - self.getDebtService()

    def getCashflowAfterTaxes(self):
        # TODO - figure out Tax Liability
        return self.getCashflowBeforeTaxes()# - self.getTaxLiability()

    def getCashOnCashReturn(self):
        return self.getCashflowAfterTaxes() / self.getInvestedCash()

    def getPricePerUnit(self):
        if self.property.units > 0:
            return self.purchase_price / self.property.units
        return "Unkown"

    def getIncomePerUnit(self):
        if self.property.units > 0:
            return self.getGrossScheduledIncome() / self.property.units
        return "Unkown"

    def getExpensesPerUnit(self):
        if self.property.units > 0:
            return self.getOperatingExpenses() / self.property.units
        return "Unkown"

    def getPricePerSquareFoot(self):
        return self.purchase_price / self.total_finished_sq_foot

    def getNetRentableAreaIncomePerSquareFoot(self):
        return self.getGrossScheduledIncome() / self.total_finished_sq_foot

    def getNetRentableAreaExpensesPerSquareFoot(self):
        return self.getOperatingExpenses() / self.total_finished_sq_foot

    def getOperatingExpenseRatio(self):
        return self.getOperatingExpenses() / self.getGrossScheduledIncome()

    def getOperatingExpenseRatioByYear(self, year):
        return self.getOperatingExpensesByYear(year) / self.getGrossOperatingIncomeByYear(year)

    def getDebtCoverageRatio(self):
        return self.getNetOperatingIncome() / self.getDebtService()

    def getBreakEvenRatio(self):
        return (self.getDebtService() + self.getOperatingExpenses()) / self.getGrossOperatingIncome()

    def getBreakEvenRatioByYear(self, year):
        return (self.getDebtService() + self.getOperatingExpensesByYear(year)) / self.getGrossOperatingIncomeByYear(year)

    def getReturnOnEquity(self):
        return self.getCashflowAfterTaxes() / self.getInvestedCash()

    #TODO - Cashflow calculations Chapter #32 and onward. http://www.wikisummaries.org/wiki/What_Every_Real_Estate_Investor_Needs_to_Know_about_Cash_Flow..._And_36_Other_Key_Financial_Measures#Chapter_6:_Calculation_1:_Simple_Interest


class Loan(db.Model, AuditMixin):
    __tablename__ = "loan"
    id = db.Column(db.Integer, primary_key=True)
    proforma_id = db.Column(db.Integer, db.ForeignKey('proforma.id'))
    type = db.Column(db.Integer)
    amount = db.Column(db.Integer, default=0)
    interest_rate = db.Column(db.Numeric(precision=6,scale=3))
    interest_only = db.Column(db.Boolean)
    length = db.Column(db.Integer)

    def getType(self):
        return PROFORMA_CONSTANTS.LOAN_TYPE[self.type]

    def getDiscountFactor(self):
        rate_per_period = Decimal(self.interest_rate) / Decimal(100) / 12
        number_of_periods = Decimal(self.length*12)
        return (((1 + rate_per_period)**number_of_periods) - 1) / (rate_per_period*(1+rate_per_period)**number_of_periods)

    def getMonthlyPayment(self):
        payment = 0
        present_value = Decimal(self.amount)
        if self.interest_only:
            payment = present_value * Decimal(self.interest_rate) / Decimal(100) / 12
        else:
            payment = present_value / self.getDiscountFactor()
        cents = Decimal('.01')
        money = payment.quantize(cents, ROUND_HALF_UP)
        return money

    def getAnnualPayment(self):
        return self.getMonthlyPayment() * 12

class LineItem(db.Model, AuditMixin):
    __tablename__ = "line_item"
    id = db.Column(db.Integer, primary_key=True)
    income_proforma_id = db.Column(db.Integer, db.ForeignKey('proforma.id'))
    expense_proforma_id = db.Column(db.Integer, db.ForeignKey('proforma.id'))
    type = db.Column(db.String(255))
    amount = db.Column(db.Integer, default=0)
    frequency = db.Column(db.Integer)
    annual_increase_perc = db.Column(db.Numeric(precision=6,scale=2))

    def getFrequency(self):
        return PROFORMA_CONSTANTS.FREQUENCY_TYPE[self.frequency]

    def getAnnualizedAmount(self):
        return self.amount * self.frequency

    def getCompoundingAmountByYear(self, year):
        principal = self.getAnnualizedAmount()
        rate = 0
        if self.annual_increase_perc is not None:
            rate = self.annual_increase_perc/100
        return principal * (1 + rate)**(year - 1)
