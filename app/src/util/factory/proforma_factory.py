from app.models.proforma import Proforma, Loan, LineItem, PercentLineItem, CapitalExpenditure
from app.models.fair_market_rent import FairMarketRent
from app.models.market import Market
from decimal import Decimal

class ProformaFactory():
    @staticmethod
    def buildProfromasFromProperty(property):
        if not property.canAutoEvaluate():
            pass
        property.addProforma(ProformaFactory.buildSection8Proforma(property))
        property.addProforma(ProformaFactory.buildMedianRentProforma(property))

    @staticmethod
    def buildSection8Proforma(property):
        proforma = Proforma()
        proforma.title = "Section 8 Rental"
        proforma.description = "Auto evaluated Section 8 rental proforma."
        proforma.seller_concessions = 0
        proforma.closing_costs = 6000
        proforma.rent_ready_costs = 3000
        proforma.initial_reserve_amount = 1000
        proforma.lease_option_fee = 0
        proforma.total_finished_sq_foot = property.sq_feet
        proforma.land_value_perc = 1
        proforma.income_tax_rate = 0
        proforma.property_appreciation_rate = 0
        proforma.vacancy_perc = 8
        proforma.sales_commission_rate = 6

        fmr = FairMarketRent.query.filter_by(zip_code=property.address.postal_code).first()
        rent = 0
        if property.bedrooms == 0:
            rent = fmr.zero_bedroom
        elif property.bedrooms == 1:
            rent = fmr.one_bedroom
        elif property.bedrooms == 2:
            rent = fmr.two_bedroom
        elif property.bedrooms == 3:
            rent = fmr.three_bedroom
        elif property.bedrooms == 4:
            rent = fmr.four_bedroom

        income = LineItem()
        income.amount = rent
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
        management.frequency = 1
        management.calculation = "GOI"

        insurance = LineItem()
        if property.property_type == 2:
            insurance.amount = 1200
        else:
            insurance.amount = 2000
        insurance.type = "Insurance"
        insurance.frequency = 1
        insurance.annual_increase_perc = 3

        proforma.addIncomeLineItem(income)
        proforma.addExpenseLineItem(taxes)
        proforma.addExpenseLineItem(insurance)
        proforma.addExpenseLineItem(management)

        max_loan_amount = ProformaFactory.getMaxLoanAmount(noi=proforma.getNetOperatingIncome(), r=0.0425/12, n=30*12, rehab=proforma.rent_ready_costs+proforma.closing_costs+proforma.rent_ready_costs+proforma.initial_reserve_amount)
        loan = Loan()
        loan.interest_only = False
        loan.interest_rate = Decimal(4.25)
        loan.amount = int(max_loan_amount)
        loan.length = 30
        loan.type = 0

        proforma.addLoan(loan)

        proforma.arv = int(max_loan_amount/.75)
        proforma.purchase_price = int(max_loan_amount/.75)

        #print(ProformaFactory.getCalculatedBalance(float(proforma.loans[0].getMonthlyPayment()), proforma.loans[0].getInterestRate(), proforma.loans[0].length * 12))

        #ProformaFactory.test(a=proforma.rent_ready_costs, d=proforma.getNetOperatingIncome(), c=10, r=0.0425/12, n=30*12)
        #ProformaFactory.getMaxLoanAmount(noi=proforma.getNetOperatingIncome(), r=0.0425/12, n=30*12, rehab=proforma.rent_ready_costs+proforma.closing_costs+proforma.rent_ready_costs+proforma.initial_reserve_amount)

        return proforma

    @staticmethod
    def buildMedianRentProforma(property):
        proforma = Proforma()
        proforma.title = "Median Rent Listing"
        proforma.description = "Auto evaluated proforma."
        proforma.seller_concessions = 0
        proforma.closing_costs = 6000
        proforma.rent_ready_costs = 3000
        proforma.initial_reserve_amount = 1000
        proforma.lease_option_fee = 0
        proforma.total_finished_sq_foot = property.sq_feet
        proforma.land_value_perc = 1
        proforma.income_tax_rate = 0
        proforma.property_appreciation_rate = 0
        proforma.vacancy_perc = 8
        proforma.sales_commission_rate = 6

        market = Market.query.filter_by(region_type=4, region_name=property.address.postal_code).first()
        if market is None:
            return
        rent = int([data_point for data_point in market.data_points if data_point.type == 64][-1].value)
        if rent is None:
            return

        income = LineItem()
        income.amount = rent
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
        management.frequency = 1
        management.calculation = "GOI"

        insurance = LineItem()
        if property.property_type == 2:
            insurance.amount = 1200
        else:
            insurance.amount = 2000
        insurance.type = "Insurance"
        insurance.frequency = 1
        insurance.annual_increase_perc = 3

        proforma.addIncomeLineItem(income)
        proforma.addExpenseLineItem(taxes)
        proforma.addExpenseLineItem(insurance)
        proforma.addExpenseLineItem(management)

        max_loan_amount = ProformaFactory.getMaxLoanAmount(noi=proforma.getNetOperatingIncome(), r=0.0425/12, n=30*12, rehab=proforma.rent_ready_costs+proforma.closing_costs+proforma.rent_ready_costs+proforma.initial_reserve_amount)
        loan = Loan()
        loan.interest_only = False
        loan.interest_rate = Decimal(4.25)
        loan.amount = int(max_loan_amount)
        loan.length = 30
        loan.type = 0

        proforma.addLoan(loan)

        proforma.arv = int(max_loan_amount/.75)
        proforma.purchase_price = int(max_loan_amount/.75)

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
        noi = float(noi)
        q = (1+r)**n
        mPay = (3*noi*r*q-3*rehab*c*r*q)/(36*r*q+c*q-c)
        principal = (mPay*q-mPay)/(r*q)
        return int(principal)
