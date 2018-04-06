import csv
import re
def fromcsv(filename):
    lines = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lines.append(row)
    return lines

fieldTypes = {'midHash', 'midZip', 'mid', 'dbaOrStreet', 'crmid'}

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
    elif (fieldType == 'crmid'):
        if not (re.match('^[a-zA-Z0-9\-]+$', string) and len(string) >= 10):
            return False
        return True
    elif (fieldType == 'dbaOrStreet'):
        if (len(string) <= 3):
            return False
        return True
    return False

locationsList = fromcsv('uniqueLocs.csv')
midsList = fromcsv('uniqueMids.csv')

print("No. of mid records: ", len(midsList)-1)
print("No. of location records: ", len(locationsList)-1)

mids = {}
midsByMid = {}
duplicateMids = 0

for i in range(1, len(midsList)):
    if (testForValidData(midsList[i][1], 'mid')):
        if (midsList[i][1] in midsByMid):
            duplicateMids += 1
            continue
        else:
            midsByMid[midsList[i][1]] = True
    mids[midsList[i][0]] = { 'id': midsList[i][0], 'name': midsList[i][11], 'mid': midsList[i][1], 'crmid': midsList[i][3], 'zip':  midsList[i][15], 'hash': midsList[i][18], 'street': midsList[i][13]}

print("No. of duplicate mids: ", duplicateMids)

# convert locs list to dicts with searchable keys

locsByCrmIdDup = 0
locsByCrmId = {}

locsByDbaNameDupe = 0
locsByDbaName = {}

locsByMidZip = {}
locsByMidZipDupe = 0

locsByMidHash = {}
locsByMidHashDupe = 0

for i in range(1, len(locationsList)):
    if (testForValidData(locationsList[i][10], 'crmid')):
        if (locationsList[i][10] in locsByCrmId):
            locsByCrmIdDup += 1
            print("crmid " + locationsList[i][10] + "exists more than once in locations data")
        else:
            locsByCrmId[locationsList[i][10]] = { 'lid': locationsList[i][1] }

    if (testForValidData(locationsList[i][2], 'dbaOrStreet') ):
        if (locationsList[i][2] in locsByDbaName):
            locsByDbaNameDupe += 1
            print("dba name " + locationsList[i][2] + " exists more than once in locations data")
        else:
            locsByDbaName[locationsList[i][2]] = { 'lid': locationsList[i][1] }

    if (testForValidData(locationsList[i][16], 'midZip') and testForValidData(locationsList[i][17], 'midZip')):
        if (locationsList[i][16] + locationsList[i][17] in locsByMidZip):
            locsByMidZipDupe += 1
            print("mid zip combo " + locationsList[i][16] + locationsList[i][17] + " exists more than once in locations data")
        else:
            locsByMidZip[locationsList[i][16] + locationsList[i][17]] = { 'lid': locationsList[i][1] }

    if (testForValidData(locationsList[i][19], 'midHash')):
        if (locationsList[i][19] in locsByMidHash):
            locsByMidHashDupe += 1
            print(locationsList[i][19])
        else:
            locsByMidHash[locationsList[i][19]] = { 'lid': locationsList[i][1] }

print("No. of locations with unique crmid: ", len(locsByCrmId.keys()))
print("No. of locations with duplicate crmid: ", locsByCrmIdDup)

print("No. of locations with a unique dba name: ", len(locsByDbaName.keys()))
print("No. of locations with duplicate dba name: ", locsByDbaNameDupe)

print("No. of locations with unique concat last 4 of mid and zip: ", len(locsByMidZip.keys()))
print("No. of locations with duplicate concat last 4 of mid and zip: ", locsByMidZipDupe)

print("No. of locations with unique mid hash: ", len(locsByMidHash.keys()))
print("No. of locations with duplicate mid hash values: ", locsByMidHashDupe)

# find matches

matchCountByCrmId = 0
matchCountByDbaName = 0
zipLast4MidMatchCount = 0
matchCountMidHash = 0

mismatchedMids = {}

for k in mids:
    if (mids[k]['crmid'] in locsByCrmId):
        mids[k]['lid'] = locsByCrmId[mids[k]['crmid']]['lid']
        mids[k]['lidMatchList'] = [{'crmid': locsByCrmId[mids[k]['crmid']]['lid']}]
        matchCountByCrmId += 1

    if (mids[k]['name'] in locsByDbaName):
        if ('lid' in mids[k]):
            if (mids[k]['lid'] != locsByDbaName[mids[k]['name']]['lid']):
                mismatchedMids[mids[k]['id']] = True
            mids[k]['lidMatchList'].append({'dbaName': locsByDbaName[mids[k]['name']]['lid']})
        else:
            mids[k]['lid'] = locsByDbaName[mids[k]['name']]['lid']
            mids[k]['lidMatchList'] = [{'dbaName': locsByDbaName[mids[k]['name']]['lid']}]

        matchCountByDbaName += 1

    if ((mids[k]['zip'] + mids[k]['mid'][-4:]) in locsByMidZip):
        if ('lid' in mids[k]):
            if (mids[k]['lid'] != locsByMidZip[mids[k]['zip'] + mids[k]['mid'][-4:]]['lid']):
                mismatchedMids[mids[k]['id']] = True
            mids[k]['lidMatchList'].append({'midZip': locsByMidZip[mids[k]['zip'] + mids[k]['mid'][-4:]]['lid']})
        else:
            mids[k]['lid'] = locsByMidZip[mids[k]['zip'] + mids[k]['mid'][-4:]]['lid']
            mids[k]['lidMatchList'] = [{'midZip': locsByMidZip[mids[k]['zip'] + mids[k]['mid'][-4:]]['lid']}]

        zipLast4MidMatchCount += 1

    if (mids[k]['hash'] in locsByMidHash):
        if ('lid' in mids[k]):
            if (mids[k]['lid'] != locsByMidHash[mids[k]['hash']]['lid']):
                mismatchedMids[mids[k]['id']] = True
            mids[k]['lidMatchList'].append({'hash': locsByMidHash[mids[k]['hash']]['lid']})
        else:
            mids[k]['lid'] = locsByMidHash[mids[k]['hash']]['lid']
            mids[k]['lidMatchList'] = [{'hash': locsByMidHash[mids[k]['hash']]['lid']}]

        matchCountMidHash += 1

print("No. of matches on Dynamics id: ", matchCountByCrmId)
print("No. of matches on dba name: ", matchCountByDbaName)
print("No. of matches on zip + last 4 of mid: ", zipLast4MidMatchCount)
print("No. of matches on mid hash: ", matchCountMidHash)
print("No. of mismatched mids: ", len(mismatchedMids.keys()))


totalMatchCount = 0
midsWithLids = open("sfMidsMappedToLids.csv", "w")
midsWithLids.write("sfId,mainDbLid,dbaName\n")

locsWithSfId = {}

for k in mids:
    if ('lid' in mids[k]):
        if (mids[k]['id'] in mismatchedMids):
            print("Sf id " + mids[k]['id'] + " matches on the following locations and field types ",
            mids[k]['lidMatchList'])
        else:
            totalMatchCount += 1
            locsWithSfId[mids[k]['lid']] = mids[k]['id']
            midsWithLids.write("\"" + mids[k]['id'] + "\",\"" + mids[k]['lid'] + "\",\"" + mids[k]['name'] + "\"\n")

midsWithLids.close()
print("No. of total matches: ", totalMatchCount)

locsHeaders = ["LocationKey","LocationId","LocationName","MerchantId","CompanyId",
"LocationContact","CreatedOn","UpdatedOn","Active","Deleted","CRMID","ForceQuarantineTypeId",
"Address1","Address2","City","State","Zip","MerchantIdLast","ClosingTime","MerchantIdSHA512",
"ResultCallbackUrl","ResultCallbackUrlTurnOnDate","BatchStartTime","BatchEndTime","BatchRetryInterval",
"CloseBatchActive","Sfid"]

locsWithSfIds = open("locsWithSfIds.csv", "w")

locsHeaderRow = locsHeaders[0]
for i in range(1, len(locsHeaders)):
    locsHeaderRow += "," + locsHeaders[i]
locsHeaderRow += "\n"

locsWithSfIds.write(locsHeaderRow)

for i in range(1, len(locationsList)):
    row = "\"" + locationsList[i][0] + "\""
    for j in range(1, len(locationsList[i])):
        row += ",\"" + locationsList[i][j] + "\""
    if (locationsList[i][1] in locsWithSfId):
        row += ",\"" + locsWithSfId[locationsList[i][1]] + "\"\n"
    else:
        row += ",\"\"\n"
    locsWithSfIds.write(row)

locsWithSfIds.close()







