import numpy as np
import png
import pydicom
import os
import shutil
import re
from natsort import natsorted

sourceDir = '_data/dicom'
dcmStudiesDir = os.path.join(sourceDir, 'dcm')
pngStudiesDir = os.path.join(sourceDir, 'png')

def convertDCMtoPNG(dcmPath, pngPath):
    ds = pydicom.dcmread(dcmPath)

    shape = ds.pixel_array.shape

    # Convert to float to avoid overflow or underflow losses.
    image_2d = ds.pixel_array.astype(float)

    # Rescaling grey scale between 0-255
    image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0

    # Convert to uint
    image_2d_scaled = np.uint8(image_2d_scaled)

    # Write the PNG file
    with open(pngPath, 'wb') as png_file:
        w = png.Writer(shape[1], shape[0], greyscale=True)
        w.write(png_file, image_2d_scaled)

# 1. Remove all png files
print('deleting ' + pngStudiesDir)
shutil.rmtree(pngStudiesDir, ignore_errors=True)
os.makedirs(pngStudiesDir)

# 2. Convert dcm files into png
for root, dirNames, fileNames in os.walk(dcmStudiesDir):
    for dirName in dirNames:
        os.makedirs(os.path.join(pngStudiesDir, dirName), exist_ok=True)
        for root, dirNames, fileNames in os.walk(os.path.join(dcmStudiesDir, dirName)):
                for fileName in natsorted(fileNames):
                        if ".dcm" in fileName.lower():
                                dcmPath = os.path.join(dcmStudiesDir, dirName, fileName)
                                number = re.findall(r'\d+', fileName)[0]
                                pngPath = os.path.join(pngStudiesDir, dirName, dirName + '_' + number + '.png')
                                print('converting ' + dcmPath + ' -> ' + pngPath)
                                convertDCMtoPNG(dcmPath, pngPath)            
    break
