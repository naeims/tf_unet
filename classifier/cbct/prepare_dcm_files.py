import numpy as np
import png
import pydicom
import os
import csv
import shutil
import re
from natsort import natsorted

sourceDir = '../../_data/dcm_raw'
targetDir = '../../_data/dcm'
mappingFile = 'mapping.csv'

# 1. Parse mapping file
mapping = {}
with open(mappingFile, mode='r') as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter=',')
        for row in csvReader:
                mapping[row['study_id']] = row['garbage_start']

print(mapping)

# 2. Delete classification data
print('deleting ' + targetDir)
shutil.rmtree(targetDir, ignore_errors=True)
os.makedirs(targetDir)

# 3. Copy files around
for root, dirNames, fileNames in os.walk(sourceDir):
        for dirName in dirNames:
                garbageStart = mapping[dirName]
                os.makedirs(os.path.join(targetDir, dirName), exist_ok=True)
                for root, dirNames, fileNames in os.walk(os.path.join(sourceDir, dirName)):
                        for fileName in natsorted(fileNames):
                                sliceNumber = re.findall(r'\d+', fileName)[0]
                                srcPath = os.path.join(sourceDir, dirName, fileName)
                                if int(sliceNumber) < int(garbageStart):
                                        dstPath = os.path.join(targetDir, dirName, fileName)
                                        print('copying ' + srcPath + ' -> ' + dstPath)
                                        shutil.copyfile(srcPath, dstPath)
                                else:
                                        print('ignoring ' + srcPath)
