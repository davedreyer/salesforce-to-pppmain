import hashlib
import csv
import re
def fromcsv(filename):
    lines = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lines.append(row)
    return lines

fieldTypes = {'midHash', 'midZip', 'mid', 'dbaOrStreet'}

def testForValidData(string, fieldType):
    if not (fieldType in fieldTypes):
        raise Exception('Invalid field type to check!')
    if (string is None):
        return False
    elif (string == ""):
        return False
    elif (string == "NULL"):
        return False
    elif (fieldType == 'midHash'):
        if not (re.match('^[a-z0-9]+$', string)):
            return False
        return True
    elif (fieldType == 'midZip'):
        if not (re.match('^[0-9\-]+$', string) and len(string) >= 4):
            return False
        return True
    elif (fieldType == 'mid'):
        if not (re.match('^[0-9]+$', string) and len(string) >= 10):
            return False
        return True
    elif (fieldType == 'dbaOrStreet'):
        if (len(string) <= 3):
            return False
        return True
    return False

locationsList = fromcsv('LocationTable.csv')
midsList = fromcsv('mids_extract_031418.csv')

print("No. of location records: ", len(locationsList)-1)
print("No. of sf mid records: ", len(midsList)-1)

locsByMidHash = {}
locsByMidHashDupeMap = {}

locsByDba = {}
locsByDbaDupeMap = {}

locsByMidZip = {}
locsByMidZipDupeMap = {}

locsByStreet = {}
locsByStreetDupeMap = {}

for i in range(1, len(locationsList)):
    if (testForValidData(locationsList[i][19], 'midHash')):
        if (locationsList[i][19] in locsByMidHash):
            locsByMidHashDupeMap[locationsList[i][19]] = True
        else:
            locsByMidHash[locationsList[i][19]] = True

    if (testForValidData(locationsList[i][2], 'dbaOrStreet')):
        if (locationsList[i][2] in locsByDba):
            locsByDbaDupeMap[locationsList[i][2]] = True
        else:
            locsByDba[locationsList[i][2]] = True

    if (testForValidData(locationsList[i][16], 'midZip') and testForValidData(locationsList[i][17], 'midZip')):
        if (locationsList[i][16] + locationsList[i][17] in locsByMidZip):
            locsByMidZipDupeMap[locationsList[i][16] + locationsList[i][17]] = True
        else:
            locsByMidZip[locationsList[i][16] + locationsList[i][17]] = True

    if (testForValidData(locationsList[i][12], 'dbaOrStreet')):
        if (locationsList[i][12].lower() in locsByStreet):
            locsByStreetDupeMap[locationsList[i][12].lower()] = True
        else:
            locsByStreet[locationsList[i][12].lower()] = True

print("No. of unique mid hash values for locations: ", len(locsByMidHash.keys()))
print("No. of mid hash values that are duplicated: ", len(locsByMidHashDupeMap.keys()))

print("No. of unique mid dba names for locations: ", len(locsByDba.keys()))
print("No. of mid dba names that are duplicated: ", len(locsByDbaDupeMap.keys()))

print("No. of unique mid + zip concat combos for locations: ", len(locsByMidZip.keys()))
print("No. of mid + zip concat combos that are duplicated: ", len(locsByMidZipDupeMap.keys()))

print("No. of unique street addresses for locations: ", len(locsByStreet.keys()))
print("No. of street addresses that are duplicated: ", len(locsByStreetDupeMap.keys()))

locsUnique = []
locsDupe = []

for i in range(1, len(locationsList)):
    if (locationsList[i][19] in locsByMidHashDupeMap):
        locsDupe.append(locationsList[i])
    elif (locationsList[i][2] in locsByDbaDupeMap):
        locsDupe.append(locationsList[i])
    elif ((testForValidData(locationsList[i][16], 'midZip') and testForValidData(locationsList[i][17], 'midZip'))
        and (locationsList[i][16] + locationsList[i][17] in locsByMidZipDupeMap)):
            locsDupe.append(locationsList[i])
        # if (locationsList[i][16] + locationsList[i][17] in locsByMidZipDupeMap):
        #     locsDupe.append(locationsList[i])
        # else:
        #     locsUnique.append(locationsList[i])
    elif (testForValidData(locationsList[i][12], 'dbaOrStreet')
        and (locationsList[i][12].lower() in locsByStreetDupeMap)):
            locsDupe.append(locationsList[i])
        # if (locationsList[i][12].lower() in locsByStreetDupeMap):
        #     locsDupe.append(locationsList[i])
        # else:
        #     locsUnique.append(locationsList[i])
    else:
        locsUnique.append(locationsList[i])

locsHeaders = ["LocationKey","LocationId","LocationName","MerchantId","CompanyId",
"LocationContact","CreatedOn","UpdatedOn","Active","Deleted","CRMID","ForceQuarantineTypeId",
"Address1","Address2","City","State","Zip","MerchantIdLast","ClosingTime","MerchantIdSHA512",
"ResultCallbackUrl","ResultCallbackUrlTurnOnDate","BatchStartTime","BatchEndTime","BatchRetryInterval",
"CloseBatchActive"]

locsDupeFile = open("dupLocs.csv", "w")
locsUniqueFile = open("uniqueLocs.csv", "w")

locsHeaderRow = locsHeaders[0]
for i in range(1, len(locsHeaders)):
    locsHeaderRow += "," + locsHeaders[i]
locsHeaderRow += "\n"

locsUniqueFile.write(locsHeaderRow)
locsDupeFile.write(locsHeaderRow)

for i in range(0, len(locsDupe)):
    row = ""
    for j in range(0, len(locsDupe[i])):
        row += "\"" + locsDupe[i][j] + "\","
    row += "\n"
    locsDupeFile.write(row)

locsDupeFile.close()

for i in range(0, len(locsUnique)):
    row = ""
    for j in range(0, len(locsUnique[i])):
        row += "\"" + locsUnique[i][j] + "\","
    row += "\n"
    locsUniqueFile.write(row)

locsUniqueFile.close()

midsByMid = {}
midsByMidDupeMap = {}

midsByDba = {}
midsByDbaDupeMap = {}

midsByMidZip = {}
midsByMidZipDupeMap = {}

midsByStreet = {}
midsByStreetDupeMap = {}

for i in range(1, len(midsList)):
    if (testForValidData(midsList[i][1], 'mid')):
        if (midsList[i][1] in midsByMid):
            midsByMidDupeMap[midsList[i][1]] = True
        else:
            midsByMid[midsList[i][1]] = True

    if (testForValidData(midsList[i][11], 'dbaOrStreet')):
        if (midsList[i][11] in midsByDba):
            midsByDbaDupeMap[midsList[i][11]] = True
        else:
            midsByDba[midsList[i][11]] = True

    if (testForValidData(midsList[i][15], 'midZip') and testForValidData(midsList[i][1], 'mid')):
        if (midsList[i][15] + midsList[i][1][-4:] in midsByMidZip):
            midsByMidZipDupeMap[midsList[i][15] + midsList[i][1][-4:]] = True
        else:
            midsByMidZip[midsList[i][15] + midsList[i][1][-4:]] = True

    if (testForValidData(midsList[i][13], 'dbaOrStreet')):
        if (midsList[i][13].lower() in midsByStreet):
            midsByStreetDupeMap[midsList[i][13].lower()] = True
        else:
            midsByStreet[midsList[i][13].lower()] = True

print("No. of unique mid values for mids: ", len(midsByMid.keys()))
print("No. of mid values that are duplicated for mids: ", len(midsByMidDupeMap.keys()))

print("No. of unique mid dba names for mids: ", len(midsByDba.keys()))
print("No. of mid dba names that are duplicated for mids: ", len(midsByDbaDupeMap.keys()))

print("No. of unique mid + zip concat combos for mids: ", len(midsByMidZip.keys()))
print("No. of mid + zip concat combos that are duplicated for mids: ", len(midsByMidZipDupeMap.keys()))

print("No. of unique street addresses for mids: ", len(midsByStreet.keys()))
print("No. of street addresses that are duplicated for mids: ", len(midsByStreetDupeMap.keys()))

midsUnique = []
midsDupe = []

for i in range(1, len(midsList)):
    if (midsList[i][1] in midsByMidDupeMap):
        midsDupe.append(midsList[i])
    elif (midsList[i][11] in midsByDbaDupeMap):
        midsDupe.append(midsList[i])
    elif ((testForValidData(midsList[i][15], 'midZip') and testForValidData(midsList[i][1], 'mid'))
        and (midsList[i][15] + midsList[i][1][-4:] in midsByMidZipDupeMap)):
            midsDupe.append(midsList[i])
        # if (midsList[i][15] + midsList[i][1][-4:] in midsByMidZipDupeMap):
        #     midsDupe.append(midsList[i])
        # else:
        #     midsUnique.append(midsList[i])
    elif (testForValidData(midsList[i][13], 'dbaOrStreet')
        and (midsList[i][13].lower() in midsByStreetDupeMap)):
            midsDupe.append(midsList[i])
        # if (midsList[i][13].lower() in midsByStreetDupeMap):
        #     midsDupe.append(midsList[i])
        # else:
        #     midsUnique.append(midsList[i])
    else:
        midsUnique.append(midsList[i])

print("Final number of unique sf mid records: ", len(midsUnique) - 1)
print("Final number of duplicated sf mid records: ", len(midsDupe) - 1)

midsDupeFile = open("dupMids.csv", "w")
midsUniqueFile = open("uniqueMids.csv", "w")

midsHeaders = ["ID","NAME","CREATEDDATE","DYNAMICS_GUID__C",
"OPPORTUNITY__R.DATE_TIME_CHANGED_TO_TO_BE_INSTALLED__C","ACCOUNT__C",
"ACCOUNT_REP__C","ACCOUNT_TYPE__C","CORPORATE_CONTACT__C","DBA_CITY__C",
"DBA_E_MAIL_ADDRESS__C","DBA_NAME__C","DBA_STATE__C","DBA_STREET_ADDRESS_1__C",
"DBA_STREET_ADDRESS_2__C","DBA_ZIP_POSTAL_CODE__C","LOCATION_PHONE_NUMBER__C","REFERRAL_ACCOUNT__C"]

midsHeaderRow = midsHeaders[0]
for i in range(1, len(midsHeaders)):
    midsHeaderRow += "," + midsHeaders[i]
midsHeaderRow += "\n"

midsUniqueFile.write(midsHeaderRow)
midsDupeFile.write(midsHeaderRow)

for i in range(0, len(midsDupe)):
    row = ""
    for j in range(0, len(midsDupe[i])):
        row += "\"" + midsDupe[i][j] + "\","
    row += "\n"
    midsDupeFile.write(row)

midsDupeFile.close()

for i in range(0, len(midsUnique)):
    row = ""
    for j in range(0, len(midsUnique[i])):
        row += "\"" + midsUnique[i][j] + "\","
    row += "\"" + hashlib.sha512(midsUnique[i][1]).hexdigest() + "\""
    row += "\n"
    midsUniqueFile.write(row)

midsUniqueFile.close()