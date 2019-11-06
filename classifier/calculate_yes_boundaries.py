# Load ressults.csv
# For each study, load all slices and their yes-ness values
# Find the slice that gives the minimum error
# Error is mean(difference^2)

import csv
import math

resultsFile = 'results.csv'

def calcError(yesnessData, step):
    sum = 0.0
    for sliceNumber in yesnessData:
        yesness = yesnessData[sliceNumber]
        sliceNumber = int(sliceNumber)
        if sliceNumber < step:
            sum = sum + math.pow(float(yesness), 2.0)
        else:
            sum = sum + math.pow((1.0 - float(yesness)), 2.0)
    return sum / len(yesnessData)

# Parse results file
data = {}
with open(resultsFile, mode='r') as csvFile:
    csvReader = csv.DictReader(csvFile, delimiter=',')
    for row in csvReader:
        studyId = row['study_id']
        if studyId not in data:
            data[studyId] = {}
        data[studyId][row['slice_number']] = row['yesness']

print('study_id,c3c4_start')
for studyId in data:
    minError = float('inf')
    minErrorStep = -1
    yesnessData = data[studyId]
    for sliceNumber in yesnessData:
        step = int(sliceNumber)
        error = calcError(yesnessData, step)
        if error < minError:
            minError = error
            minErrorStep = step
    
    print('{},{}'.format(studyId, minErrorStep))
