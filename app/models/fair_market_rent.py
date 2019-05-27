from flask import jsonify
from app import db
from app.constants import dataset as DATASET_CONSTANTS
import json

class FairMarketRent(db.Model):
    __tablename__ = "fair_market_rent"
    id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.Integer, nullable=False)
    zero_bedroom =db.Column(db.Integer, nullable=False)
    one_bedroom = db.Column(db.Integer, nullable=False)
    two_bedroom = db.Column(db.Integer, nullable=False)
    three_bedroom = db.Column(db.Integer, nullable=False)
    four_bedroom = db.Column(db.Integer, nullable=False)
