import csv
import re
def fromcsv(filename):
    lines = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lines.append(row)
    return lines

fieldTypes = {'midHash', 'midZip', 'mid', 'dba'}

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
    elif (fieldType == 'dba'):
        if (len(string) <= 3):
            return False
        return True
    return False

locationsList = fromcsv('LocationTable.csv')
midsList = fromcsv('mids_extract_031418.csv')

print("No. of location records: ", len(locationsList)-1)

locsByMidHash = {}
locsByMidHashDupeMap = {}

locsByDba = {}
locsByDbaDupeMap = {}

locsByMidZip = {}
locsByMidZipDupeMap = {}

for i in range(1, len(locationsList)):
    if (testForValidData(locationsList[i][19], 'midHash')):
        if (locationsList[i][19] in locsByMidHash):
            locsByMidHashDupeMap[locationsList[i][19]] = True
        else:
            locsByMidHash[locationsList[i][19]] = True

    if (testForValidData(locationsList[i][2], 'dba')):
        if (locationsList[i][2] in locsByDba):
            locsByDbaDupeMap[locationsList[i][2]] = True
        else:
            locsByDba[locationsList[i][2]] = True

    if (testForValidData(locationsList[i][16], 'midZip') and testForValidData(locationsList[i][17], 'midZip')):
        if (locationsList[i][16] + locationsList[i][17] in locsByMidZip):
            locsByMidZipDupeMap[locationsList[i][16] + locationsList[i][17]] = True
        else:
            locsByMidZip[locationsList[i][16] + locationsList[i][17]] = True

print("No. of unique mid hash values for locations: ", len(locsByMidHash.keys()))
print("No. of mid hash values that are duplicated: ", len(locsByMidHashDupeMap.keys()))

print("No. of unique mid dba names for locations: ", len(locsByDba.keys()))
print("No. of mid dba names that are duplicated: ", len(locsByDbaDupeMap.keys()))

print("No. of unique mid + zip concat combos for locations: ", len(locsByMidZip.keys()))
print("No. of mid + zip concat combos that are duplicated: ", len(locsByMidZipDupeMap.keys()))

locsUnique = []
locsDupe = []

for i in range(1, len(locationsList)):
    if (locationsList[i][19] in locsByMidHashDupeMap):
        locsDupe.append(locationsList[i])
    elif (locationsList[i][2] in locsByDbaDupeMap):
        locsDupe.append(locationsList[i])
    elif (locationsList[i][16] + locationsList[i][17] in locsByMidZipDupeMap):
        locsDupe.append(locationsList[i])
    else:
        locsUnique.append(locationsList[i])

locsDupeFile = open("dupLocs.csv", "w")
locsUniqueFile = open("uniqueLocs.csv", "w")

for i in range(0, len(locsDupe) - 1):
    row = ""
    for j in range(0, len(locsDupe[i]) - 1):
        row += "\"" + locsDupe[i][j] + "\","
    row += "\n"
    locsDupeFile.write(row)

locsDupeFile.close()

for i in range(0, len(locsUnique) - 1):
    row = ""
    for j in range(0, len(locsUnique[i]) - 1):
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

for i in range(1, len(midsList)):
    if (testForValidData(midsList[i][1], 'mid')):
        if (midsList[i][1] in midsByMid):
            midsByMidDupeMap[midsList[i][1]] = True
        else:
            midsByMid[midsList[i][1]] = True

    if (testForValidData(midsList[i][11], 'dba')):
        if (midsList[i][11] in midsByDba):
            midsByDbaDupeMap[midsList[i][11]] = True
        else:
            midsByDba[midsList[i][11]] = True

    if (testForValidData(midsList[i][15], 'midZip') and testForValidData(midsList[i][1], 'mid')):
        if (midsList[i][15] + midsList[i][1][-4:] in midsByMidZip):
            midsByMidZipDupeMap[midsList[i][15] + midsList[i][1][-4:]] = True
        else:
            midsByMidZip[midsList[i][15] + midsList[i][1][-4:]] = True

print("No. of unique mid values for mids: ", len(midsByMid.keys()))
print("No. of mid values that are duplicated for mids: ", len(midsByMidDupeMap.keys()))

print("No. of unique mid dba names for mids: ", len(midsByDba.keys()))
print("No. of mid dba names that are duplicated for mids: ", len(midsByDbaDupeMap.keys()))

print("No. of unique mid + zip concat combos for mids: ", len(midsByMidZip.keys()))
print("No. of mid + zip concat combos that are duplicated for mids: ", len(midsByMidZipDupeMap.keys()))

midsUnique = []
midsDupe = []

for i in range(1, len(midsList)):
    if (midsList[i][1] in midsByMidDupeMap):
        midsDupe.append(midsList[i])
    elif (midsList[i][11] in midsByDbaDupeMap):
        midsDupe.append(midsList[i])
    elif (midsList[i][15] + midsList[i][1][-4:] in midsByMidZipDupeMap):
        midsDupe.append(midsList[i])
    else:
        midsUnique.append(midsList[i])

midsDupeFile = open("dupMids.csv", "w")
midsUniqueFile = open("uniqueMids.csv", "w")

for i in range(0, len(midsDupe) - 1):
    row = ""
    for j in range(0, len(midsDupe[i]) - 1):
        row += "\"" + midsDupe[i][j] + "\","
    row += "\n"
    midsDupeFile.write(row)

midsDupeFile.close()

for i in range(0, len(midsUnique) - 1):
    row = ""
    for j in range(0, len(midsUnique[i]) - 1):
        row += "\"" + midsUnique[i][j] + "\","
    row += "\n"
    midsUniqueFile.write(row)

midsUniqueFile.close()


# def testForEmptyMidHash(string):
#     if (string is None):
#         return False
#     if not (re.match('^[a-z0-9]+$', string)):
#         return False
#     if (string == 'NULL'):
#         return False
#     return True

# def testForEmptyMidZip(string):
#     if (string is None):
#         return False
#     if not (re.match('^[a-zA-Z0-9\-]+$', string)):
#         return False
#     if (string == 'NULL'):
#         return False
#     return True

# def testForEmptyMid(string):
#     if (string is None):
#         return False
#     if not (re.match('[0-9]+$', string)):
#         return False
#     return True

# def testForEmptyDba(string):
#     if (string is None):
#         return False
#     if (string == ""):
#         return False
#     if (string == 'NULL'):
#         return False
#     return True

# locsByDba = {}
# locsByDbaDupeMap = {}

# for i in range(1, len(locationsList)):
#     if (testForEmptyDba(locationsList[i][2])):
#         if (locationsList[i][2] in locsByDba):
#             locsByDbaDupeMap[locationsList[i][2]] = True
#             continue
#         locsByDba[locationsList[i][2]] = { 'lid': locationsList[i][1] }
# print("No. of unique mid dba names for locations: ", len(locsByDba.keys()))
# print("No. of mid dba names that are duplicated: ", len(locsByDbaDupeMap.keys()))

# locsByMidZip = {}
# locsByMidZipDupeMap = {}

# for i in range(1, len(locationsList)):
#     if (testForEmptyMidZip(locationsList[i][16]) and testForEmpty(locationsList[i][17])):
#         if (locationsList[i][16] + locationsList[i][17] in locsByMidZip):
#             locsByMidZipDupeMap[locationsList[i][16] + locationsList[i][17]] = True
#             continue
#         locsByMidZip[locationsList[i][16] + locationsList[i][17]] = { 'lid': locationsList[i][1] }
# print("No. of unique mid + zip concat combos for locations: ", len(locsByMidZip.keys()))
# print("No. of mid + zip concat combos that are duplicated: ", len(locsByMidZipDupeMap.keys()))