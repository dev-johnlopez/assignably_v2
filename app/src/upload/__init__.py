import pandas as pd
import numpy as np
import re
from app import db
from flask import flash
from flask_security import current_user
from app.models.contact import Contact
from app.models.address import Address
from app.models.property import Property
from app.src.util.date_util import createDateFromString
from pandas import ExcelFile

listsource_headers = [
    'OWNER 1 LAST NAME',
    'OWNER 1 FIRST NAME',
    'OWNER 1 MIDDLE NAME',
    'OWNER 1 SUFFIX',
    'OWNER 2 LAST NAME',
    'OWNER 2 FIRST NAME',
    'OWNER 2 MIDDLE NAME',
    'OWNER 2 SUFFIX',
    'MAIL ADDRESS',
    'MAIL CITY',
    'MAIL STATE'
    'MAIL ZIP CODE',
    'MAIL ZIP+4',
    'PROPERTY ADDRESS',
    'PROPERTY CITY',
    'PROPERTY STATE',
    'PROPERTY ZIP CODE',
    'PROPERTY ZIP+4',
    'PROPERTY TYPE',
    'EQUITY (%)',
    'BLDG/LIVING AREA',
    'BEDROOMS',
    'LAST MARKET SALE DATE',
    'OWNER OCCUPIED',
    'PHONE NUMBER',
]


def upload_leads(fileData, user):
    if fileData is not None:
        df = readExcel(fileData, user)
        if validDataFrame(df, listsource_headers):
            mapProperties(df, user)

def upload_lead_dataframe(dataFrame, user):
    if validDataFrame(dataFrame, listsource_headers):
        mapProperties(dataFrame, user)

def validDataFrame(df, headers):
    return pd.Series(headers).isin(df).any()

def readExcel(fileData, user):
    df = pd.read_excel(fileData, sheet_name=0)
    df1 = df.replace(np.nan, '', regex=True)
    df2 = df1.replace({r'[^\x00-\x7F]+':''}, regex=True)
    return df2

def mapProperties(df, user):
    total_rows = len(df.index)
    for index, row in df.iterrows():
        processRow(row)
    user.add_notification('bulk_upload_complete', None)
    db.session.commit()

def processRow(row):
    mailing_address = mapAddress(row, "MAIL")
    owner1 = mapOwner(row, "1", mailing_address)
    owner2 = mapOwner(row, "2", mailing_address)
    owners = [owner1, owner2]
    property_address = mapAddress(row, "PROPERTY")
    property = mapProperty(row, property_address)
    property.addOwners([owner1, owner2])
    if mailing_address.compareTo(property_address) is False:
        mailing_property = mapProperty(None, mailing_address)
        mailing_property.addOwners(owners)
        db.session.add(mailing_property)
    db.session.add(property)


def mapOwner(dfRow, owner_number, mailing_address):
    owner_full_name = str(dfRow["OWNER {} LABEL NAME".format(owner_number)])
    first_name = str(dfRow["OWNER {} FIRST NAME".format(owner_number)])
    last_name = str(dfRow["OWNER {} LAST NAME".format(owner_number)])
    contact_type = "lead"

    if owner_full_name is None or owner_full_name is "":
        return None

    owner = getOwnerRecordIfDuplicateExists(first_name, last_name, contact_type, mailing_address)
    if owner is not None:
        print("********: WARNING - DUPLICATE OWNER FOUND")
        return owner

    return Contact(
        first_name = first_name,
        last_name = last_name,
        contact_type = contact_type,
        mailing_address = mailing_address
    )

def getOwnerRecordIfDuplicateExists(first_name, last_name, contact_type, mailing_address):
    matching_contacts = Contact.query.filter_by(
            first_name=first_name,
            last_name=last_name,
            contact_type=contact_type).all()
    for contact in matching_contacts:
        if contact.mailing_address.compareTo(mailing_address):
            return contact
    return None

def mapAddress(dfRow, addressType):
    #house_number = str(dfRow["{} HOUSE NUMBER".format(addressType)]).strip()
    line_1 = str(dfRow["{} ADDRESS".format(addressType)]).strip()
    city = str(dfRow["{} CITY".format(addressType)]).strip()
    state_code = str(dfRow["{} STATE".format(addressType)]).strip()
    postal_code = str(dfRow["{} ZIP CODE".format(addressType)]).strip()
    matching_addresses = Address.query.filter_by(
        line_1 = line_1,
        city = city,
        state_code = state_code,
        postal_code = postal_code
    ).all()

    if len(matching_addresses) > 1:
        print("********: ERROR - DUPLICATE ADDRESSES FOUND")

    if len(matching_addresses) is 1:
        print("********: WARNING - DUPLICATE ADDRESSES FOUND")
        return matching_addresses[0]

    return Address(
        line_1 = line_1,
        city = city,
        state_code = state_code,
        postal_code = postal_code
    )

def mapProperty(dfRow, address):
    property = getExistingPropertyOrNew(address)
    if dfRow is not None:
        updatePropertyDetails(property, dfRow)
    else:
        property.owner_occupied = True

    return property

def getExistingPropertyOrNew(address):
    property = Property.query.join(Address).filter(Address.id==address.id).first()
    if property is None:
        property = Property(address=address)
    return property

def updatePropertyDetails(property, dfRow):
    property.property_type = 0 # TODO - Map from excel
    property.sq_feet = str(dfRow["BLDG/LIVING AREA"])
    property.bedrooms = str(dfRow["BEDROOMS"])
    property.last_sale_date = createDateFromString("/", str(dfRow["LAST MARKET SALE DATE"]))
    property.owner_occupied = True if str(dfRow["OWNER OCCUPIED"]) else False
