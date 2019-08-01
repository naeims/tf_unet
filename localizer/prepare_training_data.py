# Load mapping.csv
# Make dir data/training
# For every study that is in the training set
#    Copy each file from _data/png into _data/localizer_training, e.g. 10_49.png
#    Copy labels from _data/raw_labels into _data/localizer_training, e.g. 10_49_mask.png
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
labelDir = '../_data/raw_labels'
trainingDir = '../_data/localizer_training'
saveDir = 'data/labels'
mappingFile = '../classifier/cbct/mapping.csv'
ignoreMargin = 7
ignoreWholeHead = True

# Delete dirs
print('deleting ' + trainingDir)
shutil.rmtree(trainingDir, ignore_errors=True)
os.makedirs(trainingDir)

print('deleting ' + saveDir)
shutil.rmtree(saveDir, ignore_errors=True)
os.makedirs(saveDir)

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
                    continue

                # copy image
                srcPath = os.path.join(imageDir, dirName, fileName)
                dstPath = os.path.join(trainingDir, fileName)
                shutil.copyfile(srcPath, dstPath)

                # process label
                labelPath = os.path.join(labelDir, dirName, fileName)
                if os.path.exists(labelPath):
                    print('Label found! Converting {}'.format(labelPath))

                    labelIm = Image.open(labelPath)
                    labelArr = np.asarray(labelIm)
                    shape = np.shape(labelArr)

                    maskArr = np.zeros([shape[0], shape[1]], np.float32)

                    for x in range(shape[0]):
                        for y in range(shape[1]):
                            if not (labelArr[x, y, 0] == labelArr[x, y, 1] and labelArr[x, y, 1] == labelArr[x, y, 2]):
                                maskArr[x, y] = 255.0

                    maskFileName = fileName.replace('.png', '_mask.png')
                    maskPath = os.path.join(trainingDir, maskFileName)

                    with open(maskPath, 'wb') as png_file:
                        w = png.Writer(shape[1], shape[0], greyscale=True)
                        w.write(png_file, np.uint8(maskArr))
                    
                    # make backup
                    shutil.copyfile(maskPath, os.path.join(saveDir, maskFileName))

                else:
                    print('No label found, assuming all black {}'.format(labelPath))
                    im = Image.open(srcPath)
                    arr = np.asarray(im)
                    shape = np.shape(arr)
                    maskArr = np.zeros([shape[0], shape[1]], np.float32)
                    maskFileName = fileName.replace('.png', '_mask.png')
                    maskPath = os.path.join(trainingDir, maskFileName)

                    with open(maskPath, 'wb') as png_file:
                        w = png.Writer(shape[1], shape[0], greyscale=True)
                        w.write(png_file, np.uint8(maskArr))

    break