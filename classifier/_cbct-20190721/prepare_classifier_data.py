import numpy as np
import png
import pydicom
import os
import csv
import shutil
import re
from natsort import natsorted

sourceDir = '../../_data/dicom/jpg'
targetDir = '../../_data/dicom/classify'
yesTargetDir = os.path.join(targetDir, 'cbctyes')
noTargetDir = os.path.join(targetDir, 'cbctno')
mappingFile = 'mapping.csv'
testSet = ['13', '14', '15', '16']

# 1. Parse mapping file
mapping = {}
with open(mappingFile, mode='r') as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter=',')
        for row in csvReader:
                mapping[row['study_id']] = row['c3c4_start']

print(mapping)

# 2. Delete classification data
print('deleting ' + targetDir)
shutil.rmtree(targetDir, ignore_errors=True)
os.makedirs(targetDir)
os.makedirs(yesTargetDir)
os.makedirs(noTargetDir)

# 3. Copy files around
for root, dirNames, fileNames in os.walk(sourceDir):
        for dirName in dirNames:
                if dirName in testSet:
                        continue
                c3c4Start = mapping[dirName]
                for root, dirNames, fileNames in os.walk(os.path.join(sourceDir, dirName)):
                        for fileName in natsorted(fileNames):
                                sliceNumber = re.findall(r'_\d+', fileName)[0][1:]
                                srcPath = os.path.join(sourceDir, dirName, fileName)
                                dstPath = ''
                                if int(sliceNumber) < int(c3c4Start):
                                        dstPath = os.path.join(noTargetDir, fileName)
                                else:
                                        dstPath = os.path.join(yesTargetDir, fileName)
                                print('copying ' + srcPath + ' -> ' + dstPath)
                                shutil.copyfile(srcPath, dstPath)

