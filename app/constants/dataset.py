# Data Provider
UNKNOWN = 0
ZILLOW = 1
HUD = 2
PROVIDER_NAME = {
  UNKNOWN: 'Unknown',
  ZILLOW: 'Zillow',
  HUD: 'HUD'
}

# Region Type
METRO_US = 0
STATE = 1
COUNTY = 2
CITY = 3
ZIP_CODE = 4
NEIGHBORHOOD = 5
REGION_TYPE = {
  METRO_US: 'Metro & U.S.',
  STATE: 'State',
  COUNTY: 'County',
  CITY: 'City',
  ZIP_CODE: 'Zip Code',
  NEIGHBORHOOD: 'Neighborhood'
}

# Dataset Type
ZHVI_SUMMARY = 0
ZHVI_ALL_HOMES_TIME_SERIES = 1
ZHVI_ALL_HOMES_BOTTOM_TIER_TIME_SERIES = 2
ZHVI_ALL_HOMES_TOP_TIER_TIME_SERIES = 3
ZHVI_CONDO_TIME_SERIES = 4
ZHVI_SFH_TIME_SERIES = 5
ZHVI_1BR_TIME_SERIES = 6
ZHVI_2BR_TIME_SERIES = 7
ZHVI_3BR_TIME_SERIES = 8
ZHVI_4BR_TIME_SERIES = 9
ZHVI_5BR_PLUS_TIME_SERIES = 10
MEDIAN_HOME_VALUE_PER_SQFT = 11
ZILLOW_HOME_VALUE_FORECAST = 12
QUARTERLY_HISTORIC_METRO_ZHVI = 13
INCREASING_VALUES_PERC = 14
DECREASING_VALUES_PERC = 15
MEDIAN_SALES_PRICE_SEASONALLY_ADJUSTED = 16
MONTHLY_HOME_SALES_SEASONALLY_ADJUSTED = 17
MONTHLY_HOME_SALES_RAW = 18
MEDIAN_LIST_PRICE = 19
MEDIAN_LIST_PRICE_TOP_TIER = 20
MEDIAN_LIST_PRICE_BOTTOM_TIER = 21
MEDIAN_LIST_PRICE_PER_SQFT = 22
MEDIAN_LIST_PRICE_PER_SQFT_TOP_TIER = 23
MEDIAN_LIST_PRICE_PER_SQFT_BOTTOM_TIER = 24
LISTINGS_WITH_PRICE_CUT = 25
LISTINGS_WITH_PRICE_CUT_SEASONALLY_ADJUSTED = 26
LISTINGS_WITH_PRICE_CUT_SEASONALLY_ADJUSTED_SFR = 27
LISTINGS_WITH_PRICE_CUT_SEASONALLY_ADJUSTED_CONDO = 28
LISTINGS_WITH_PRICE_CUT_SEASONALLY_ADJUSTED_TOP_TIER = 29
LISTINGS_WITH_PRICE_CUT_SEASONALLY_ADJUSTED_MIDDLE_TIER = 30
LISTINGS_WITH_PRICE_CUT_SEASONALLY_ADJUSTED_BOTTON_TIER = 31
MEDIAN_PRICE_CUT = 32
BUYER_SELLER_INDEX_CROSS_TIME = 33
BUYER_SELLER_INDEX_CROSS_REGION = 34
DAYS_ON_ZILLOW = 35
SALE_TO_LIST_RATIO = 36
FORECLOSURE_RESALES = 37
MONTHLY_FOR_SALE_INVENTORY_RAW = 38
MONTHLY_FOR_SALE_INVENTORY_SEASONALLY_ADJUSTED = 39
MONTHLY_FOR_SALE_INVENTORY_TOP_TIER_SEASONALLY_ADJUSTED = 40
MONTHLY_FOR_SALE_INVENTORY_MIDDLE_TIER_SEASONALLY_ADJUSTED = 41
MONTHLY_FOR_SALE_INVENTORY_BOTTOM_TIER_SEASONALLY_ADJUSTED = 42
AGE_OF_INVENTORY = 43
NEW_MONTHLY_FOR_SALE_INVENTORY_RAW = 44
NEW_MONTHLY_FOR_SALE_INVENTORY_SEASONALLY_ADJUSTED = 45
MEDIAN_DAILY_FOR_SALE_INVENTORY_RAW = 46
MEDIAN_DAILY_FOR_SALE_INVENTORY_SEASONALLY_ADJUSTED = 47
ZRI_SUMMARY = 48
ZRI_TIME_SERIES = 49
ZRI_TIME_SERIES_SFH = 50
ZRI_TIME_SERIES_MULTI = 51
MEDIAN_ZRI_PER_SQFT = 52
PRICE_TO_RENT_RATIO = 53
QUARLERY_HISTORIC_METRO_ZRI = 54
ZILLOW_RENT_FORECAST = 55
MEDIAN_RENT_LIST_PRICE_NON_MULTI = 56
MEDIAN_RENT_LIST_PRICE_MULTIFAMILY_FIVE_PLUS = 57
MEDIAN_RENT_LIST_PRICE_CONDO = 58
MEDIAN_RENT_LIST_PRICE_DUPLEX_TRIPLEX = 59
MEDIAN_RENT_LIST_PRICE_SFH = 60
MEDIAN_RENT_LIST_PRICE_STUDIO = 61
MEDIAN_RENT_LIST_PRICE_1BR = 62
MEDIAN_RENT_LIST_PRICE_2BR = 63
MEDIAN_RENT_LIST_PRICE_3BR = 64
MEDIAN_RENT_LIST_PRICE_4BR = 65
MEDIAN_RENT_LIST_PRICE_5BR_PLUS = 66
MEDIAN_RENT_LIST_PRICE_PER_SQFT_NON_MULTI = 67
MEDIAN_RENT_LIST_PRICE_PER_SQFT_MULTIFAMILY_FIVE_PLUS = 68
MEDIAN_RENT_LIST_PRICE_PER_SQFT_CONDO = 69
MEDIAN_RENT_LIST_PRICE_PER_SQFT_DUPLEX_TRIPLEX = 70
MEDIAN_RENT_LIST_PRICE_PER_SQFT_SFH = 71
MEDIAN_RENT_LIST_PRICE_PER_SQFT_STUDIO = 72
MEDIAN_RENT_LIST_PRICE_PER_SQFT_1BR = 73
MEDIAN_RENT_LIST_PRICE_PER_SQFT_2BR = 74
MEDIAN_RENT_LIST_PRICE_PER_SQFT_3BR = 75
MEDIAN_RENT_LIST_PRICE_PER_SQFT_4BR = 76
MEDIAN_RENT_LIST_PRICE_PER_SQFT_5BR_PLUS = 77
FMR = 78
DATASET_TYPE = {
    ZHVI_SUMMARY: 'ZHVI Summary (Current Month)',
    ZHVI_ALL_HOMES_TIME_SERIES: 'ZHVI All Homes (SFR, Condo/Co-op) Time Series ($)',
    ZHVI_ALL_HOMES_BOTTOM_TIER_TIME_SERIES: 'ZHVI All Homes- Bottom Tier Time Series ($)',
    ZHVI_ALL_HOMES_TOP_TIER_TIME_SERIES: 'ZHVI All Homes- Top Tier Time Series ($)',
    ZHVI_CONDO_TIME_SERIES: 'ZHVI Condo/Co-op Time Series ($)',
    ZHVI_SFH_TIME_SERIES: 'ZHVI Single-Family Homes Time Series ($)',
    ZHVI_1BR_TIME_SERIES: 'ZHVI 1-Bedroom Time Series ($)',
    ZHVI_2BR_TIME_SERIES: 'ZHVI 2-Bedroom Time Series ($)',
    ZHVI_3BR_TIME_SERIES: 'ZHVI 3-Bedroom Time Series ($)',
    ZHVI_4BR_TIME_SERIES: 'ZHVI 4-Bedroom Time Series ($)',
    ZHVI_5BR_PLUS_TIME_SERIES: 'ZHVI 5+ Bedroom Time Series ($)',
    MEDIAN_HOME_VALUE_PER_SQFT: 'Median Home Value Per Sq Ft ($)',
    ZILLOW_HOME_VALUE_FORECAST: 'Zillow Home Value Forecast',
    QUARTERLY_HISTORIC_METRO_ZHVI: 'Quarterly Historic Metro ZHVI',
    INCREASING_VALUES_PERC: 'Increasing Values (%)',
    DECREASING_VALUES_PERC: 'Decreasing Values (%)',
    MEDIAN_SALES_PRICE_SEASONALLY_ADJUSTED: 'Median Sale Price - Seasonally Adjusted ($)',
    MONTHLY_HOME_SALES_SEASONALLY_ADJUSTED: 'Monthly Home Sales (Number, Seasonally Adjusted)',
    MONTHLY_HOME_SALES_RAW: 'Monthly Home Sales (Number, Raw)',
    MEDIAN_LIST_PRICE: 'Median List Price ($)',
    MEDIAN_LIST_PRICE_TOP_TIER: 'Median List Price - Top Tier ($)',
    MEDIAN_LIST_PRICE_BOTTOM_TIER: 'Median List Price - Bottom Tier ($)',
    MEDIAN_LIST_PRICE_PER_SQFT: 'Median List Price Per Sq Ft ($)',
    MEDIAN_LIST_PRICE_PER_SQFT_TOP_TIER: 'Median List Price Per Sq Ft - Top Tier ($)',
    MEDIAN_LIST_PRICE_PER_SQFT_BOTTOM_TIER: 'Median List Price Per Sq Ft - Bottom Tier ($)',
    LISTINGS_WITH_PRICE_CUT: 'Listings with Price Cut (%)',
    LISTINGS_WITH_PRICE_CUT_SEASONALLY_ADJUSTED: 'Listings With Price Cut - Seasonally Adjusted (%)',
    LISTINGS_WITH_PRICE_CUT_SEASONALLY_ADJUSTED_SFR: 'Listings With Price Cut - Seasonally Adjusted, SFR (%)',
    LISTINGS_WITH_PRICE_CUT_SEASONALLY_ADJUSTED_CONDO: 'Listings With Price Cut - Seasonally Adjusted, Condo/Co-op (%)',
    LISTINGS_WITH_PRICE_CUT_SEASONALLY_ADJUSTED_TOP_TIER: 'Listings With Price Cut - Seasonally Adjusted, Top-Tier (%)',
    LISTINGS_WITH_PRICE_CUT_SEASONALLY_ADJUSTED_MIDDLE_TIER: 'Listings With Price Cut - Seasonally Adjusted, Middle-Tier (%)',
    LISTINGS_WITH_PRICE_CUT_SEASONALLY_ADJUSTED_BOTTON_TIER: 'Listings WIth Price Cut - Seasonally Adjusted, Bottom-Tier (%)',
    MEDIAN_PRICE_CUT: 'Median Price Cut (%)',
    BUYER_SELLER_INDEX_CROSS_TIME: 'Buyer-Seller Index (Cross-Time)',
    BUYER_SELLER_INDEX_CROSS_REGION: 'Buyer-Seller Index (Cross-Region)',
    DAYS_ON_ZILLOW: 'Days on Zillow',
    SALE_TO_LIST_RATIO: 'Sale-to-list ratio',
    FORECLOSURE_RESALES: 'Foreclosure Re-sales (%)',
    MONTHLY_FOR_SALE_INVENTORY_RAW: 'Monthly For-Sale Inventory (Raw)',
    MONTHLY_FOR_SALE_INVENTORY_SEASONALLY_ADJUSTED: 'Monthly For-Sale Inventory (Smooth, Seasonally Adjusted)',
    MONTHLY_FOR_SALE_INVENTORY_TOP_TIER_SEASONALLY_ADJUSTED: 'Monthly For-Sale Inventory Top Tier (Smooth, Seasonally Adjusted)',
    MONTHLY_FOR_SALE_INVENTORY_MIDDLE_TIER_SEASONALLY_ADJUSTED: 'Monthly For-Sale Inventory Middle Tier (Smooth, Seasonally Adjusted)',
    MONTHLY_FOR_SALE_INVENTORY_BOTTOM_TIER_SEASONALLY_ADJUSTED: 'Monthly For-Sale Inventory Bottom Tier (Smooth, Seasonally Adjusted)',
    AGE_OF_INVENTORY: 'Age of Inventory (Days)',
    NEW_MONTHLY_FOR_SALE_INVENTORY_RAW: 'New Monthly For-Sale Inventory (Raw)',
    NEW_MONTHLY_FOR_SALE_INVENTORY_SEASONALLY_ADJUSTED: 'New Monthly For-Sale Inventory (Smooth, Seasonally Adjusted)',
    MEDIAN_DAILY_FOR_SALE_INVENTORY_RAW: 'Median Daily For-Sale Inventory (Raw)',
    MEDIAN_DAILY_FOR_SALE_INVENTORY_SEASONALLY_ADJUSTED: 'Median Daily For-Sale Inventory (Smooth, Seasonally Adjusted)',
    ZRI_SUMMARY: 'ZRI Summary: Multifamily, SFR, Condo/Co-op (Current Month)',
    ZRI_TIME_SERIES: 'ZRI Time Series: Multifamily, SFR, Condo/Co-op ($)',
    ZRI_TIME_SERIES_SFH: 'ZRI Time Series: SFR ($)',
    ZRI_TIME_SERIES_MULTI: 'ZRI Time Series: Multifamily ($)',
    MEDIAN_ZRI_PER_SQFT: 'Median ZRI Per Sq Ft: SFR, Condo/Co-op ($)',
    PRICE_TO_RENT_RATIO: 'Price-to-Rent Ratio',
    QUARLERY_HISTORIC_METRO_ZRI: 'Quarterly Historic Metro ZRI',
    ZILLOW_RENT_FORECAST: 'Zillow Rent Forecast',
    MEDIAN_RENT_LIST_PRICE_NON_MULTI: 'Median Rent List Price ($), SFR, Condo/Co-op',
    MEDIAN_RENT_LIST_PRICE_MULTIFAMILY_FIVE_PLUS: 'Median Rent List Price ($), Multifamily 5+ units',
    MEDIAN_RENT_LIST_PRICE_CONDO: 'Median Rent List Price ($), Condo/Co-op',
    MEDIAN_RENT_LIST_PRICE_DUPLEX_TRIPLEX: 'Median Rent List Price ($), Duplex/Triplex',
    MEDIAN_RENT_LIST_PRICE_SFH: 'Median Rent List Price ($), Single-Family Residence',
    MEDIAN_RENT_LIST_PRICE_STUDIO: 'Median Rent List Price ($), Studio',
    MEDIAN_RENT_LIST_PRICE_1BR: 'Median Rent List Price ($), 1-Bedroom',
    MEDIAN_RENT_LIST_PRICE_2BR: 'Median Rent List Price ($), 2-Bedroom',
    MEDIAN_RENT_LIST_PRICE_3BR: 'Median Rent List Price ($), 3-Bedroom',
    MEDIAN_RENT_LIST_PRICE_4BR: 'Median Rent List Price ($), 4-Bedroom',
    MEDIAN_RENT_LIST_PRICE_5BR_PLUS: 'Median Rent List Price ($), 5+ Bedroom',
    MEDIAN_RENT_LIST_PRICE_PER_SQFT_NON_MULTI: 'Median Rent List Price ($ Per Sq. Foot), SFR, Condo/Co-op',
    MEDIAN_RENT_LIST_PRICE_PER_SQFT_MULTIFAMILY_FIVE_PLUS: 'Median Rent List Price ($ Per Sq. Foot), Multifamily 5+ units',
    MEDIAN_RENT_LIST_PRICE_PER_SQFT_CONDO: 'Median Rent List Price ($ Per Sq. Foot), Condo/Co-op',
    MEDIAN_RENT_LIST_PRICE_PER_SQFT_DUPLEX_TRIPLEX: 'Median Rent List Price ($ Per Sq. Foot), Duplex/Triplex',
    MEDIAN_RENT_LIST_PRICE_PER_SQFT_SFH: 'Median Rent List Price ($ Per Sq. Foot), Single-Family Residence',
    MEDIAN_RENT_LIST_PRICE_PER_SQFT_STUDIO: 'Median Rent List Price ($ Per Sq. Foot), Studio',
    MEDIAN_RENT_LIST_PRICE_PER_SQFT_1BR: 'Median Rent List Price ($ Per Sq. Foot), 1-Bedroom',
    MEDIAN_RENT_LIST_PRICE_PER_SQFT_2BR: 'Median Rent List Price ($ Per Sq. Foot), 2-Bedroom',
    MEDIAN_RENT_LIST_PRICE_PER_SQFT_3BR: 'Median Rent List Price ($ Per Sq. Foot), 3-Bedroom',
    MEDIAN_RENT_LIST_PRICE_PER_SQFT_4BR: 'Median Rent List Price ($ Per Sq. Foot), 4-Bedroom',
    MEDIAN_RENT_LIST_PRICE_PER_SQFT_5BR_PLUS: 'Median Rent List Price ($ Per Sq. Foot), 5+ Bedroom',
    FMR: 'Fair Market Rents'

}
