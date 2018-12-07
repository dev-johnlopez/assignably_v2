import datetime

def createDateFromString(delimeter, date_string):
    dateVals = date_string.split(delimeter)
    return datetime.date(int(dateVals[2]), int(dateVals[0]), int(dateVals[1]))
