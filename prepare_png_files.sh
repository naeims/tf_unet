#!/bin/bash

# For all directories in _data/dicom/dcm
#   - Make a directory in _data/dicom/png
#   - Convert all *.dcm files into *.png files
#
# After running this, a human must manually update _data/dicom/mapping.csv.
# When done, run prepare_classifier_data.sh


python ./prepare_png_files.py
