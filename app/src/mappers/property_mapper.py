from app.deals.models import Property

class PropertyMapper():
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
