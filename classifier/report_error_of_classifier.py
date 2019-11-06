# Compares values in mapping.csv & yes_boundaries.csv
# Reports a single error quantity over all studies
# Lower is better
# First attempt was around 1133.4

import csv
import math

mappingFile = '../data_pipeline/mapping.csv'
yesBoundariesFile = 'yes_boundaries.csv'
ignoreWholeHead = True # keep in sync with prepare_classifier_data.py

# Parse mapping file
mapping = {}
with open(mappingFile, mode='r') as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter=',')
        for row in csvReader:
                mapping[row['study_id']] = row

# Parse yes_boundaries file
yesBoundaries = {}
with open(yesBoundariesFile, mode='r') as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter=',')
        for row in csvReader:
                yesBoundaries[row['study_id']] = row

e = 0
count = 0
for studyId in yesBoundaries:
    if ignoreWholeHead == True and mapping[studyId]['is_whole_head'] == '1':
        continue
    if mapping[studyId]['is_classifier_training'] == '1': # ignore training set
        continue

    studyError = int(yesBoundaries[studyId]['c3c4_start']) - int(mapping[studyId]['c3c4_start'])
    print('study {} error {}'.format(studyId, studyError))
    e = e + math.pow(studyError, 2)
    count = count + 1

print('overall error {}'.format(e / count))