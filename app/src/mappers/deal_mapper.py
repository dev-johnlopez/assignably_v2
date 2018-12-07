from app.deals.models import Deal
from app.src.util.date_util import DateUtil

class DealMapper():
    @classmethod
    def buildDeal(self, address, type, equity, sq_feet, bedrooms, last_sale_date, owner_occupied):
        last_sale_date = DateUtil.createDateFromString("/", last_sale_date)
        property = self.buildProperty(address, type, sq_feet, bedrooms, last_sale_date, owner_occupied)
        return Deal(
            property=property,
            equity=equity
        )

    @classmethod
    def buildProperty(self, address, type, sq_feet, bedrooms, last_sale_date, owner_occupied):
        return Property(
            address=address,
            type=type,
            sq_feet=sq_feet,
            bedrooms=bedrooms,
            last_sale_date=last_sale_date,
            owner_occupied=owner_occupied
        )
