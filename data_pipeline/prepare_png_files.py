import numpy as np
import png
import pydicom
import os
import shutil
import re
import sys
from PIL import Image
from natsort import natsorted

sourceDir = '../_data'
dcmStudiesDir = os.path.join(sourceDir, 'dcm')
pngStudiesDir = os.path.join(sourceDir, 'png')
pngColorStudiesDir = os.path.join(sourceDir, 'png_color')
jpgStudiesDir = os.path.join(sourceDir, 'jpg')

def convertDCMtoPNGandJPG(dcmPath, pngPath, pngColorPath, jpgPath):
    ds = pydicom.dcmread(dcmPath)

    shape = ds.pixel_array.shape

    # Convert to float to avoid overflow or underflow losses.
    image_2d = ds.pixel_array.astype(float)
    
    # Rescaling grey scale between 0-255
    #if int(ds.RescaleSlope) != 1 or int(ds.RescaleIntercept) != 0:

    center = int(ds.WindowCenter)
    width = int(ds.WindowWidth)
    min = center - width / 2
    max = center + width / 2
    image_2d[image_2d < min] = min
    image_2d[image_2d > max] = max
    image_2d_scaled = ((image_2d - min) * (1. / (max - min)) * 255.).astype('uint8')

    # Convert to uint
    image_2d_scaled = np.uint8(image_2d_scaled)
    image_2d_color = np.repeat(image_2d_scaled, 3, axis=1)

    # Write the PNG file
    with open(pngPath, 'wb') as png_file:
        w = png.Writer(shape[1], shape[0], greyscale=True)
        w.write(png_file, image_2d_scaled)

    # Write the PNG color file
    with open(pngColorPath, 'wb') as png_color_file:
        w = png.Writer(shape[1], shape[0], greyscale=False)
        w.write(png_color_file, image_2d_color)

    # Write JPG file
    im = Image.fromarray(image_2d_scaled)
    im.save(jpgPath, quality=100);


# 1. Remove all png/jpg files
print('deleting ' + pngStudiesDir)
shutil.rmtree(pngStudiesDir, ignore_errors=True)
os.makedirs(pngStudiesDir)

print('deleting ' + pngColorStudiesDir)
shutil.rmtree(pngColorStudiesDir, ignore_errors=True)
os.makedirs(pngColorStudiesDir)

print('deleting ' + jpgStudiesDir)
shutil.rmtree(jpgStudiesDir, ignore_errors=True)
os.makedirs(jpgStudiesDir)

# 2. Convert dcm files into png
for root, dirNames, fileNames in os.walk(dcmStudiesDir):
    for dirName in dirNames:
        os.makedirs(os.path.join(pngStudiesDir, dirName), exist_ok=True)
        os.makedirs(os.path.join(pngColorStudiesDir, dirName), exist_ok=True)
        os.makedirs(os.path.join(jpgStudiesDir, dirName), exist_ok=True)
        for root, dirNames, fileNames in os.walk(os.path.join(dcmStudiesDir, dirName)):
            for fileName in natsorted(fileNames):
                if ".dcm" in fileName.lower():
                    dcmPath = os.path.join(dcmStudiesDir, dirName, fileName)
                    number = re.findall(r'\d+', fileName)[0]
                    pngPath = os.path.join(pngStudiesDir, dirName, dirName + '_' + number + '.png')
                    pngColorPath = os.path.join(pngColorStudiesDir, dirName, dirName + '_' + number + '.png')
                    jpgPath = os.path.join(jpgStudiesDir, dirName, dirName + '_' + number + '.jpg')
                    print('converting ' + dcmPath)
                    convertDCMtoPNGandJPG(dcmPath, pngPath, pngColorPath, jpgPath)
    break
