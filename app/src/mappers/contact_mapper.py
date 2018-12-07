from app.crm.models import Contact, Investor, Builder, Wholesaler, Realtor, PropertyManager, Lender

class ContactMapper():
    @classmethod
    def buildContactWithSubtype(self, first_name, last_name, phone, email, type, contact, user):
        if contact is None:
            if type == "Investor":
                contact = Investor()
            elif type == "Builder":
                contact = Builder()
            elif type == "Wholesaler":
                contact = Wholesaler()
            elif type == "Realtor":
                contact = Realtor()
            elif type == "Property Manager":
                contact = PropertyManager()
            elif type == "Lender":
                contact = Lender()
            else:
                contact = Contact()
            contact.investment_criteria=[]
            user.contacts.append(contact)
        contact.first_name=first_name
        contact.last_name=last_name
        contact.phone=phone
        contact.email=email
        return contact
