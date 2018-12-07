from app.deals.models import Address

class AddressMapper():
    @classmethod
    def buildSimpleAddress(self, line_1, line_2, line_3, line_4, city, state_code, postal_code, county, country):
        return Address(
            line_1 = line_1,
            line_2 = line_2,
            line_3 = line_3,
            line_4 = line_4,
            city = city,
            state_code = state_code,
            postal_code = postal_code,
            county = county,
            country = country
        )

    @classmethod
    def buildDetailedAddress(self, line_1, line_2, line_3, line_4, city, state_code, postal_code, country):
        return Address(
            line_1 = line_1,
            line_2 = line_2,
            line_3 = line_3,
            line_4 = line_4,
            city = city,
            state_code = state_code,
            postal_code = postal_code,
            country = country
        )
