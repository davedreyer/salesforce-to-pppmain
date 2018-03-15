import csv
import re
def fromcsv(filename):
    lines = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lines.append(row)
    return lines

def testForEmpty(string):
    if (string is None):
        return False
    if not (re.match('^[a-zA-Z0-9\-]+$', string)):
        return False
    if (string == 'NULL'):
        return False
    return True

def testForEmptyDba(string):
    if (string is None):
        return False
    if (string == ""):
        return False
    if (string == 'NULL'):
        return False
    return True    

locationsList = fromcsv('uniqueLocs.csv')
midsList = fromcsv('mids_open.csv')

print("No. of mid records: ", len(midsList)-1)
print("No. of location records: ", len(locationsList)-1)

# set up mid and locs objects

mids = {}
for i in range(1, len(midsList)):
    mids[midsList[i][0]] = { 'id': midsList[i][0], 'name': midsList[i][11], 'mid': midsList[i][1], 'cd': midsList[i][2], 'did': midsList[i][3], 'dtbi':  midsList[i][4], 'zip':  midsList[i][15], 'hash': midsList[i][18]}
print("No. of mid objects: ", len(mids.keys()))

locs = {}
for i in range(1, len(locationsList)):
    locs[locationsList[i][1]] = { 'lid': locationsList[i][1], 'name': locationsList[i][2], 'crmid': locationsList[i][10]}
print("No. of location objects: ", len(locs.keys()))

# set up locs objects with searchable keys

locsByCrmIdDup = 0
locsByCrmId = {}
for i in range(1, len(locationsList)):
    if (testForEmpty(locationsList[i][10])):  
        if (locationsList[i][10] in locsByCrmId):
            locsByCrmIdDup += 1
            print("crmid ", locationsList[i][10], " exists more than once in locations data")
            continue
        locsByCrmId[locationsList[i][10]] = { 'lid': locationsList[i][1] }
print("No. of location objects with crmid: ", len(locsByCrmId.keys()))
print("No. of locations with duplicate crmid: ", locsByCrmIdDup)

locsByDbaNameDupe = 0
locsByDbaName = {}
for i in range(1, len(locationsList)):
    if (testForEmptyDba(locationsList[i][2])):       
        if (locationsList[i][2] in locsByDbaName):
            locsByDbaNameDupe += 1
            print("dba name ", locationsList[i][2], " exists more than once in locations data")
            continue        
        locsByDbaName[locationsList[i][2]] = { 'lid': locationsList[i][1] }
print("No. of location objects with a dba name: ", len(locsByDbaName.keys()))
print("No. of locations with duplicate dba name: ", locsByDbaNameDupe)

locsByMidZip = {}
locsByMidZipDupe = 0
for i in range(1, len(locationsList)):    
    if ((testForEmpty(locationsList[i][16]) and testForEmpty(locationsList[i][17]))):
        if (locationsList[i][16] + locationsList[i][17] in locsByMidZip):
            locsByMidZipDupe += 1
            print("mid zip combo", locationsList[i][16] + locationsList[i][17], " exists more than once in locations data")
            continue
        locsByMidZip[locationsList[i][16] + locationsList[i][17]] = { 'lid': locationsList[i][1] }
print("No. of location objects with concat last 4 of mid and zip: ", len(locsByMidZip.keys()))
print("No. of locations with duplicate concat last 4 of mid and zip: ", locsByMidZipDupe)

locsByMidHash = {}
locsByMidHashDupe = 0
for i in range(1, len(locationsList)):    
    if (testForEmpty(locationsList[i][19])):
        if (locationsList[i][19] in locsByMidHash):
            locsByMidHashDupe += 1
            print(locationsList[i][19])
            # print("mid hash value", locationsList[i][19], " exists more than once in locations data")
            continue
        locsByMidHash[locationsList[i][19]] = { 'lid': locationsList[i][1] }
print("No. of location objects with a mid hash: ", len(locsByMidHash.keys()))
print("No. of locations with duplicate mid hash values: ", locsByMidHashDupe)



# find matches

matchCountByCrmId = 0
for k in mids:
    if (mids[k]['did'] in locsByCrmId):
        mids[k]['lid'] = locsByCrmId[mids[k]['did']]['lid']
        matchCountByCrmId += 1
print("No. of matches on Dynamics id: ", matchCountByCrmId)

matchCountByDbaName = 0
for k in mids:
    if (mids[k]['name'] in locsByDbaName):
        mids[k]['lid'] = locsByDbaName[mids[k]['name']]['lid']
        matchCountByDbaName += 1
print("No. of matches on dba name: ", matchCountByDbaName)

zipLast4MidMatchCount = 0
for k in mids:    
    if ((mids[k]['zip'] + mids[k]['mid'][-4:]) in locsByMidZip):
        mids[k]['lid'] = locsByMidZip[mids[k]['zip'] + mids[k]['mid'][-4:]]['lid']        
        zipLast4MidMatchCount += 1                       
print("No. of matches on zip + last 4 of mid: ", zipLast4MidMatchCount)

matchCountMidHash = 0
for k in mids:
    if (mids[k]['hash'] in locsByMidHash):
        mids[k]['lid'] = locsByMidHash[mids[k]['hash']]['lid']
        matchCountMidHash += 1
print("No. of matches on mid hash: ", matchCountMidHash)


totalMatchCount = 0
midsWithLids = open("sfMidsMappedToLids.csv", "w")
midsWithLids.write("sfId,mainDbLid,dbaName\n")

for k in mids:
    if ('lid' in mids[k] and mids[k]['lid']):        
        totalMatchCount += 1
        midsWithLids.write(mids[k]['id'] + "," + mids[k]['lid'] + "," + mids[k]['name'] + "\n")

midsWithLids.close()        
print("No. of total matches: ", totalMatchCount)






