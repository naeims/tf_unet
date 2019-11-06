import numpy as np
import png
import pydicom
import os
import csv
import shutil
import re
from natsort import natsorted

sourceDir = '../_data/jpg'
targetDir = '../_data/classifier_training'
yesTargetDir = os.path.join(targetDir, 'cbctyes')
noTargetDir = os.path.join(targetDir, 'cbctno')
mappingFile = 'mapping.csv'
ignoreWholeHead = True # keep in sync with report_error_of_classifier.py
ignoreMargin = 7 # keep in sync with label_all_images.py

# 1. Parse mapping file
mapping = {}
with open(mappingFile, mode='r') as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter=',')
        for row in csvReader:
                mapping[row['study_id']] = row

print(mapping)

# 2. Delete classification data
print('deleting ' + targetDir)
shutil.rmtree(targetDir, ignore_errors=True)
os.makedirs(targetDir)
os.makedirs(yesTargetDir)
os.makedirs(noTargetDir)

# 3. Copy files around
for root, dirNames, fileNames in os.walk(sourceDir):
        for dirName in natsorted(dirNames):
                c3c4Start = mapping[dirName]['c3c4_start']
                isWholeHead = mapping[dirName]['is_whole_head']
                isTraining = mapping[dirName]['is_classifier_training']

                if ignoreWholeHead == True and isWholeHead == '1':
                        print('Skipping because it is whole head:', dirName)
                        continue

                if isTraining == '0':
                        print('Skipping because it is not in training set:', dirName)
                        continue

                root, dirNames, fileNames = next(os.walk(os.path.join(sourceDir, dirName)))
                fileCount = len(fileNames)
                if fileCount <= 2 * ignoreMargin:
                        print('Skipping because not enough slices:', dirName)
                        continue

                print('Processing:', dirName)
                for fileName in natsorted(fileNames)[ignoreMargin:-ignoreMargin]:
                        sliceNumber = re.findall(r'_\d+', fileName)[0][1:]
                        srcPath = os.path.join(sourceDir, dirName, fileName)
                        dstPath = ''
                        if int(sliceNumber) < int(c3c4Start):
                                dstPath = os.path.join(noTargetDir, fileName)
                        else:
                                dstPath = os.path.join(yesTargetDir, fileName)
                        #print('copying ' + srcPath + ' -> ' + dstPath)
                        shutil.copyfile(srcPath, dstPath)

