#!/bin/bash

# For all directories in _data/dicom/png
#   - Use mapping.csv to determine which png files are C3/C4 and which are not
#   - Move all C3/C4 files into _data/dicom/cbct_c3c4
#   - Move all non C3/C4 files into _data/dicom/non_cbct_c3c4

# Then, separate both categories into training & test sets and copy them to TBD.
# Then we run classifier training to create the model.

python ./prepare_classifier_data.py