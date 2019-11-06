# Load mapping.csv
# Make dir data/training
# For every study that is in the training set
#    Copy each file from _data/png into _data/localizer_training, e.g. 10_49.png
#    Copy labels from _data/labels_raw into _data/localizer_training, e.g. 10_49_mask.png
#       --- convert greyscale+red to black+white
#       --- for every non-black label, put a copy in data/labels

import png
import os
import shutil
import re
import sys
import csv
import numpy as np
from PIL import Image
from natsort import natsorted

imageDir = '../_data/png'
labelDir = '../_data/labels_raw'
trainingDir = '../_data/localizer_training'
trainingDirPositive = os.path.join(trainingDir, 'positive')
trainingDirAll = os.path.join(trainingDir, 'all')
mappingFile = '../data_pipeline/mapping.csv'
ignoreMargin = 7
ignoreWholeHead = True
ignoreNegativeStudies = False
negativeMod = 10

# Delete dirs
print('deleting ' + trainingDir)
shutil.rmtree(trainingDir, ignore_errors=True)
os.makedirs(trainingDir)
os.makedirs(trainingDirPositive)
os.makedirs(trainingDirAll)

# Parse mapping file
mapping = {}
with open(mappingFile, mode='r') as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter=',')
        for row in csvReader:
                mapping[row['study_id']] = row

# Copy studies and labels
for root, dirNames, fileNames in os.walk(imageDir): 
    for dirName in natsorted(dirNames): # for each study
        if mapping[dirName]['is_localizer_training'] == '0':
            print('Skipping because not in training set: {}'.format(dirName))
            continue
        if (ignoreWholeHead == True and mapping[dirName]['is_whole_head'] == '1'):
            print('Skipping because whole head: {}'.format(dirName))
            continue

        print('Processing: {}'.format(dirName))

        for root, dirNames, fileNames in os.walk(os.path.join(imageDir, dirName)):
            for fileName in natsorted(fileNames)[ignoreMargin:-ignoreMargin]: # for each file
                sliceNumber = re.findall(r'_\d+', fileName)[0][1:]
                if int(sliceNumber) < int(mapping[dirName]['c3c4_start']):
                    print('Skipping study {} slice number {} because it is above c3c4 start'.format(dirName, sliceNumber))
                    continue

                srcPath = os.path.join(imageDir, dirName, fileName)
                dstPathAll = os.path.join(trainingDirAll, fileName)
                dstPathPositive = os.path.join(trainingDirPositive, fileName)

                labelPath = os.path.join(labelDir, dirName, fileName)

                # if no cac study, assume all black
                if mapping[dirName]['has_cac'] == '0':
                    if ignoreNegativeStudies == True:
                        print('Skipping study {} because ignoreNegativeStudies is set'.format(dirName))
                        continue
                    if int(sliceNumber) % negativeMod != 0:
                        print('Skipping study {} slice number {} to avoid too many negative samples'.format(dirName, sliceNumber))
                        continue
                    print('No CAC study {}, assuming all black {}'.format(dirName, labelPath))
                    shutil.copyfile(srcPath, dstPathAll)
                    im = Image.open(srcPath)
                    arr = np.asarray(im)
                    shape = np.shape(arr)
                    maskArr = np.zeros([shape[0], shape[1]], np.float32)
                    maskFileName = fileName.replace('.png', '_mask.png')
                    maskPath = os.path.join(trainingDirAll, maskFileName)

                    with open(maskPath, 'wb') as png_file:
                        w = png.Writer(shape[1], shape[0], greyscale=True)
                        w.write(png_file, np.uint8(maskArr))

                # process label
                elif os.path.exists(labelPath):
                    labelIm = Image.open(labelPath)
                    labelArr = np.asarray(labelIm)
                    shape = np.shape(labelArr)

                    maskArr = np.zeros([shape[0], shape[1]], np.float32)
                    hasLabeledPixel = False

                    for x in range(shape[0]):
                        for y in range(shape[1]):
                            if not (labelArr[x, y, 0] == labelArr[x, y, 1] and labelArr[x, y, 1] == labelArr[x, y, 2]):
                                maskArr[x, y] = 255.0
                                hasLabeledPixel = True

                    if hasLabeledPixel == True:
                        print('Label found! {}'.format(labelPath))
                        shutil.copyfile(srcPath, dstPathPositive)
                        maskFileName = fileName.replace('.png', '_mask.png')
                        maskPath = os.path.join(trainingDirPositive, maskFileName)

                        with open(maskPath, 'wb') as png_file:
                            w = png.Writer(shape[1], shape[0], greyscale=True)
                            w.write(png_file, np.uint8(maskArr))
                        
                    else:
                        print('No label, ignoring {}'.format(labelPath))
    break

# Copy everything from positive dir to all dir
for root, dirNames, fileNames in os.walk(trainingDirPositive):
    for fileName in natsorted(fileNames):
        srcPath = os.path.join(trainingDirPositive, fileName)
        dstPath = os.path.join(trainingDirAll, fileName)
        print('Copying {} -> {}'.format(srcPath, dstPath))
        shutil.copyfile(srcPath, dstPath)
