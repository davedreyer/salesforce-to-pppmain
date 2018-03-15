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

midsList = fromcsv('mids.csv')  

with open('sfIdsWithMidHash.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(1, len(midsList)):
        hash = hashlib.sha512(midsList[i][1]).hexdigest()        
        writer.writerow([midsList[i][0],hash])



