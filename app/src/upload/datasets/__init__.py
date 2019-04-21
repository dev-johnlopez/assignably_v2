import pandas as pd
import numpy as np
import datetime
from app.models.market import Market, DataPoint

def mapMarket(df, dfRow, dataset_type, region_type):
    #region_id = str(dfRow["RegionID"]) if "RegionID" in df.columns else None
    market = getMarket(df, dfRow, dataset_type, region_type)
    market.clearDataPoints(dataset_type=dataset_type)
    market = mapDataPoints(df, dfRow, market, dataset_type)
    return market

def mapDataPoints(df, dfRow, market, dataset_type):
    d = datetime.date.today()
    current_year = d.year
    current_month = d.strftime('%m')
    for year in range(2010, int(current_year)):
        for month in range(1, 12):
            date_string = "{}-{}".format(str(year), str(month).zfill(2))
            if date_string in df.columns:
                value = dfRow[date_string]
                if value is "":
                    value = None
                else:
                    value = float(value)
                data_point = DataPoint(
                    type = dataset_type,
                    year = year,
                    month = month,
                    value = value
                )
                market.addDataPoint(data_point)
    return market

def getValueByKey(df, dfRow, key):
    return str(dfRow[key]) if key in df.columns else None

def getMarket(df, dfRow, dataset_type, region_type):
    region_id = getValueByKey(df, dfRow, "RegionID")
    region_name = getValueByKey(df, dfRow, "RegionName")
    city = getValueByKey(df, dfRow, "City")
    state = getValueByKey(df, dfRow, "State")
    metro = getValueByKey(df, dfRow, "Metro")
    county = getValueByKey(df, dfRow, "CountyName")
    size_rank = getValueByKey(df, dfRow, "SizeRank")

    #not all data sets have a region id. Need to query without. Size Rank can change
    market = Market.query.filter_by(
        region_type = region_type,
        region_name = region_name,
        city = city,
        state = state,
        metro = metro,
        county = county
    ).first()

    if market is None:
        market = Market(
            region_id = region_id,
            region_type = region_type,
            region_name = region_name,
            city = city,
            state = state,
            metro = metro,
            county = county,
            size_rank = size_rank
        )
    else:
        market.size_rank = size_rank

    return market
