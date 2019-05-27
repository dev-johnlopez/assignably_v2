import pandas as pd
import numpy as np
import re
from app import db
from flask import flash
from flask_security import current_user
from app.models.fair_market_rent import FairMarketRent
from pandas import ExcelFile

headers = [
    'ZIP\nCode',
    'SAFMR\n0BR',
    'SAFMR\n1BR',
    'SAFMR\n2BR',
    'SAFMR\n3BR',
    'SAFMR\n4BR'
]

def getValueByKey(df, dfRow, key):
    return str(dfRow[key]) if key in df.columns else None

def mapRecord(df, dfRow):
    zip_code = getValueByKey(df, dfRow, 'ZIP\nCode')
    zero_bedroom = getValueByKey(df, dfRow, 'SAFMR\n0BR')
    one_bedroom = getValueByKey(df, dfRow, 'SAFMR\n1BR')
    two_bedroom = getValueByKey(df, dfRow, 'SAFMR\n2BR')
    three_bedroom = getValueByKey(df, dfRow, 'SAFMR\n3BR')
    four_bedroom = getValueByKey(df, dfRow, 'SAFMR\n4BR')

    fmr = FairMarketRent.query.filter_by(zip_code=zip_code)
    if fmr is not None:
        fmr.zero_bedroom = zero_bedroom
        fmr.one_bedroom = one_bedroom
        fmr.two_bedroom = two_bedroom
        fmr.three_bedroom = three_bedroom
        fmr.four_bedroom = four_bedroom
        return fmr

    return FairMarketRent(
        zip_code = zip_code,
        zero_bedroom = zero_bedroom,
        one_bedroom = one_bedroom,
        two_bedroom = two_bedroom,
        three_bedroom = three_bedroom,
        four_bedroom = four_bedroom
    )
