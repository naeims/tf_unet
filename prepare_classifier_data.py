import numpy as np
import png
import pydicom
import os
import csv
import shutil
import re
from natsort import natsorted

sourceDir = '_data/dicom/png'
targetDir = '_data/dicom/classify'
c3c4TargetDir = os.path.join(targetDir, 'cbct_c3c4')
nonc3c4TargetDir = os.path.join(targetDir, 'cbct_non_c3c4')
mappingFile = '_data/dicom/mapping.csv'

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
os.makedirs(c3c4TargetDir)
os.makedirs(nonc3c4TargetDir)

# 3. Copy files around
for root, dirNames, fileNames in os.walk(sourceDir):
        for dirName in dirNames:
                c3c4Start = mapping[dirName]
                for root, dirNames, fileNames in os.walk(os.path.join(sourceDir, dirName)):
                        for fileName in natsorted(fileNames):
                                sliceNumber = re.findall(r'_\d+', fileName)[0][1:]
                                srcPath = os.path.join(sourceDir, dirName, fileName)
                                dstPath = ''
                                if int(sliceNumber) < int(c3c4Start):
                                        dstPath = os.path.join(nonc3c4TargetDir, fileName)
                                else:
                                        dstPath = os.path.join(c3c4TargetDir, fileName)
                                print('copying ' + srcPath + ' -> ' + dstPath)
                                shutil.copyfile(srcPath, dstPath)

