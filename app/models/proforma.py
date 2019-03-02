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
    capital_expenditures = db.relationship('CapitalExpenditure')

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

    def addCapitalExpenditure(self, capital_expenditure):
        if self.capital_expenditures is None:
            self.capital_expenditures = []
        self.capital_expenditures.append(capital_expenditure)

    def getCapitalExpenditureAmount(self, year=None):
        capital_expenditure_amount = 0
        for capital_expenditure in self.capital_expenditures:
            capital_expenditure_amount += capital_expenditure.getYearlyReserve()
        return capital_expenditure_amount

    def getInvestedCash(self):
        return self.purchase_price  + self.closing_costs \
                + self.rent_ready_costs + self.initial_reserve_amount \
                - self.getTotalLoanAmount()- self.seller_concessions

    def getTotalLoanAmount(self):
        total_loan_amount = 0
        for loan in self.loans:
            total_loan_amount += loan.amount
        return total_loan_amount

    def getDebtService(self, year=None):
        debt_service_total = 0
        for loan in self.loans:
            debt_service_total += loan.getAnnualPayment(year)
        return debt_service_total

    def getGrossScheduledIncome(self, year=None):
        income_total = 0
        for line_item in self.income:
            income_total += line_item.getAnnualizedAmount(year)
        return income_total

    def getGrossRentMultiplier(self, year=None):
        return self.purchase_price / self.getGrossScheduledIncome(year)

    def getVacancyAndCreditLoss(self, year=None):
        return self.getGrossScheduledIncome(year) * self.vacancy_perc / 100

    def getGrossOperatingIncome(self, year=None):
        return self.getGrossScheduledIncome(year) - self.getVacancyAndCreditLoss(year)

    def getOperatingExpenses(self, year=None):
        expense_total = 0
        for line_item in self.expenses:
            expense_total += line_item.getAnnualizedAmount(year)
        return expense_total

    def getNetOperatingIncome(self, year=None):
        return self.getGrossOperatingIncome(year) - self.getOperatingExpenses(year)

    def getCapitalizationRate(self, year=None):
        # TODO - Cap Rate should be based on aquisition costs not arv.
        return self.getNetOperatingIncome(year) / self.purchase_price

    def getNetIncomeMultiplier(self, year=None):
        return 1 / self.getCapitalizationRate(year)

    def getPresentValue(self, year=None):
        return self.getNetIncomeMultiplier(year) * self.getNetOperatingIncome(year)

    def getDepreciationAmount(self, year=None):
        improvement_amount = self.purchase_price - (self.purchase_price * self.land_value_perc/100)
        depreciation_amount = 0
        if self.property.property_type is 4 or self.property.property_type is 5 or self.property.property_type is 6 or self.property.property_type is 7:
            depreciation_amount = improvement_amount/Decimal(39.5)
        else:
            if year is None or year < 28:
                depreciation_amount = improvement_amount/Decimal(27.5)
            elif year is 28:
                depreciation_amount = improvement_amount/Decimal(27.5/2)
        return depreciation_amount

    def getCashflowFromDepreciation(self, year=None):
        return self.getDepreciationAmount(year) * self.income_tax_rate/100

    def getTaxableIncome(self, year=None):
        #TODO - Net Operating Income less Mortgage Interest less Depreciation, Real property less Depreciation, Capital Additions less Amortization, Points and Closing Costs plus Interest Earned = Taxable Income
        return self.getNetOperatingIncome(year)

    def getCashflowBeforeTaxes(self, year=None):
        #TODO - Net Operating Income less Debt Service less Capital Additions plus Loan Proceeds plus Interest Earned
        return self.getNetOperatingIncome(year) - self.getDebtService(year)

    def getCashflowAfterTaxes(self, year=None):
        # TODO - figure out Tax Liability
        return self.getCashflowBeforeTaxes(year)# - self.getTaxLiability()

    def getCashflowAfterCapEx(self, year=None):
        return self.getCashflowBeforeTaxes(year) - self.getCapitalExpenditureAmount(year)

    def getCashflowWithDepreciation(self, year=None):
        return self.getCashflowAfterCapEx(year) + self.getCashflowFromDepreciation(year)

    def getCashOnCashReturn(self, year=None):
        return self.getCashflowAfterTaxes(year) / self.getInvestedCash() * 100

    def getCashOnCashReturnAfterCapex(self, year=None):
        return self.getCashflowAfterCapEx(year) / self.getInvestedCash() * 100

    def getCashOnCashReturnIncludingDepreciation(self, year=None):
        return self.getCashflowWithDepreciation(year) / self.getInvestedCash() * 100

    def getPricePerUnit(self):
        if self.property.units > 0:
            return self.purchase_price / self.property.units
        return "Unkown"

    def getIncomePerUnit(self, year=None):
        if self.property.units > 0:
            return self.getGrossScheduledIncome(year) / self.property.units
        return "Unkown"

    def getExpensesPerUnit(self, year=None):
        if self.property.units > 0:
            return self.getOperatingExpenses(year) / self.property.units
        return "Unkown"

    def getPricePerSquareFoot(self):
        return self.purchase_price / self.total_finished_sq_foot

    def getNetRentableAreaIncomePerSquareFoot(self, year=None):
        return self.getGrossScheduledIncome(year) / self.total_finished_sq_foot

    def getNetRentableAreaExpensesPerSquareFoot(self, year=None):
        return self.getOperatingExpenses(year) / self.total_finished_sq_foot

    def getOperatingExpenseRatio(self, year=None):
        return self.getOperatingExpenses(year) / self.getGrossOperatingIncome(year)

    def getDebtCoverageRatio(self, year=None):
        debt_service = self.getDebtService(year)
        if debt_service is 0:
            return "Infinite"
        return self.getNetOperatingIncome(year) / self.getDebtService(year)

    def getBreakEvenRatio(self, year=None):
        return (self.getDebtService(year) + self.getOperatingExpenses(year)) / self.getGrossOperatingIncome(year)

    def getReturnOnEquity(self, year=None):
        return self.getCashflowAfterTaxes(year) / self.getInvestedCash()

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

    def getAnnualPayment(self, year=None):
        if year is not None and year > self.length:
            return 0
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

    def getAnnualizedAmount(self, year=None):
        principal = self.amount * self.frequency
        if year is None:
            return principal
        rate = 0
        if self.annual_increase_perc is not None:
            rate = self.annual_increase_perc/100
        return principal * (1 + rate)**(year - 1)

class CapitalExpenditure(db.Model, AuditMixin):
    __tablename__ = "capital_expenditure"
    id = db.Column(db.Integer, primary_key=True)
    proforma_id = db.Column(db.Integer, db.ForeignKey('proforma.id'))
    type = db.Column(db.String(255))
    replacement_cost = db.Column(db.Numeric(precision=12,scale=2))
    lifespan = db.Column(db.Integer)

    def getYearlyReserve(self):
        return self.replacement_cost / self.lifespan

    def getMonthlyReserve(self):
        return self.getYearlyReserve() / 12
