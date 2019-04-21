from flask import jsonify
from app import db
from app.constants import dataset as DATASET_CONSTANTS
import json

class Market(db.Model):
    __tablename__ = "market"
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer)
    region_type = db.Column(db.Integer, nullable=False)
    region_name = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    metro = db.Column(db.String(255))
    county = db.Column(db.String(255))
    size_rank = db.Column(db.Integer)
    data_points = db.relationship("DataPoint", back_populates="market")

    def addDataPoint(self, data_point):
        if self.data_points is None:
            self.data_points = []
        self.data_points.append(data_point)

    def clearDataPoints(self, dataset_type=None):
        if self.data_points is None:
            pass
        data_points = [data_point for data_point in self.data_points if data_point.type==dataset_type and dataset_type is not None]
        for data_point in data_points:
            self.data_points.remove(data_point)
            db.session.delete(data_point)

    @property
    def serialize(self):
       return {
            'id' :  self.id,
            'region_id' : self.region_id,
            'region_type' : self.region_type,
            'region_name' : self.region_name,
            'city' : self.city,
            'state' : self.state,
            'metro' : self.metro,
            'county' : self.county,
            'size_rank' : self.size_rank,
            'dataPoints' : [data_point.serialize for data_point in self.data_points]#jsonify([data_point.serialize for data_point in self.data_points])
       }

class DataPoint(db.Model):
    __tablename__ = "datapoint"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=True)
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'))
    market = db.relationship("Market", back_populates="data_points")
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    value = db.Column(db.Numeric(precision=5,scale=2))

    def getDate(self):
        return "{} {}".format(self.month, self.year)

    def getType(self):
        return DATASET_CONSTANTS.DATASET_TYPE[self.type]

    @property
    def serialize(self):
       return {
            'id' :  self.id,
            'type' : self.type,
            'year' : self.year,
            'month' : self.month,
            'value' : str(self.value)
       }
