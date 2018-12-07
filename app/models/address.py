from flask import current_app
from app import db, geolocator
from app.mixins.audit import AuditMixin

class Address(db.Model, AuditMixin):
    id = db.Column(db.Integer, primary_key=True)
    line_1 = db.Column(db.String(255))
    line_2 = db.Column(db.String(255))
    line_3 = db.Column(db.String(255))
    line_4 = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state_code = db.Column(db.String(2))
    postal_code = db.Column(db.String(20))
    county = db.Column(db.String(255))
    country = db.Column(db.String(255))
    latitude = db.Column(db.Numeric(precision=9,scale=6))
    longitude = db.Column(db.Numeric(precision=9,scale=6))

    def __init__(self, **kwargs):
        super(Address, self).__init__(**kwargs)
        self.geocode(**kwargs)

    def __repr__(self):
        return '{}, {}, {} {}'.format(self.line_1, self.city, self.state_code, self.postal_code)

    def geocode(self, **kwargs):
        line_1 = kwargs.get("line_1",self.line_1)
        city = kwargs.get("city",self.city)
        state_code = kwargs.get("state_code",self.state_code)
        postal_code = kwargs.get("postal_code",self.postal_code)
        self.latitude = None
        self.longitude = None
        try:
            location = geolocator.geocode('{} {} {} {}'.format(line_1, city, state_code, postal_code))
            if location is not None:
                self.latitude = location.latitude
                self.longitude = location.longitude
        except:
            current_app.logger.error('Unable to geocode address')

    def compareTo(self, address):
        return self.line_1 == address.line_1 \
                and self.line_2 == address.line_2 \
                and self.line_3 == address.line_3 \
                and self.line_4 == address.line_4 \
                and self.city == address.city \
                and self.state_code == address.state_code \
                and self.postal_code == address.postal_code
