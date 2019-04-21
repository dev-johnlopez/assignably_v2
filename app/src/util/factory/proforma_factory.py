from app.models.proforma import Proforma, Loan, LineItem, PercentLineItem, CapitalExpenditure
from decimal import Decimal

class ProformaFactory():
    @staticmethod
    def buildProfromasFromProperty(property):
        if not property.canAutoEvaluate():
            pass
        property.addProforma(ProformaFactory.buildSection8Proforma(property))

    @staticmethod
    def buildSection8Proforma(property):
        proforma = Proforma()
        proforma.title = "Section 8 Rental"
        proforma.description = "Auto evaluated Section 8 rental proforma."
        proforma.arv = 120000
        proforma.purchase_price = 90000
        proforma.seller_concessions = 0
        proforma.closing_costs = 6000
        proforma.rent_ready_costs = 3000
        proforma.initial_reserve_amount = 1000
        proforma.lease_option_fee = 0
        proforma.total_finished_sq_foot = 950
        proforma.land_value_perc = 1
        proforma.income_tax_rate = 0
        proforma.property_appreciation_rate = 0
        proforma.vacancy_perc = 8
        proforma.sales_commission_rate = 6



        income = LineItem()
        income.amount = 1400
        income.type = "Rent"
        income.frequency = 12
        income.annual_increase_perc = 3

        taxes = LineItem()
        taxes.amount = property.property_tax
        taxes.type = "Taxes"
        taxes.frequency = 1
        taxes.annual_increase_perc = 3

        management = PercentLineItem()
        management.amount = 9
        management.type = "Management"
        management.frequency = 12
        management.calculation = "GOI"

        insurance = LineItem()
        insurance.amount = property.property_tax * .02
        insurance.type = "Insurance"
        insurance.frequency = 1
        insurance.annual_increase_perc = 3

        proforma.addIncomeLineItem(income)
        proforma.addExpenseLineItem(taxes)
        proforma.addExpenseLineItem(insurance)
        #proforma.addExpenseLineItem(management)

        max_loan_amount = ProformaFactory.getMaxLoanAmount(noi=proforma.getNetOperatingIncome(), r=0.0425/12, n=30*12, rehab=proforma.rent_ready_costs+proforma.closing_costs+proforma.rent_ready_costs+proforma.initial_reserve_amount)
        loan = Loan()
        loan.interest_only = False
        loan.interest_rate = 4.25
        loan.amount = max_loan_amount
        loan.length = 30
        loan.type = 0

        proforma.addLoan(loan)

        proforma.arv = int(max_loan_amount/.75)
        proforma.purchase_price = int(max_loan_amount/.75)

        #print(ProformaFactory.getCalculatedBalance(float(proforma.loans[0].getMonthlyPayment()), proforma.loans[0].getInterestRate(), proforma.loans[0].length * 12))

        #ProformaFactory.test(a=proforma.rent_ready_costs, d=proforma.getNetOperatingIncome(), c=10, r=0.0425/12, n=30*12)
        #ProformaFactory.getMaxLoanAmount(noi=proforma.getNetOperatingIncome(), r=0.0425/12, n=30*12, rehab=proforma.rent_ready_costs+proforma.closing_costs+proforma.rent_ready_costs+proforma.initial_reserve_amount)

        return proforma

    def getMaxAllowableOffer(proforma):
        p = 500
        return (proforma.getNetOperatingIncome(0) - p*500) / (proforma.rent_ready_costs + ProformaFactory.getCalculatedBalance(p, .0425, 360))
        increment = 100000
        current_offer = 0
        max_offer = 0

    @staticmethod
    def getCalculatedBalance(p, rate, n):
        return (p * (1 - (1/(1 + rate)**n))) / rate

    @staticmethod
    def getMaxLoanAmount(noi, r, rehab, n, c=0.1):
        q = (1+r)**n
        mPay = (3*noi*r*q-3*rehab*c*r*q)/(36*r*q+c*q-c)
        principal = (mPay*q-mPay)/(r*q)
        return int(principal)
