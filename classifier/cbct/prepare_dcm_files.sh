#!/bin/bash

# For all directories in _data/dicom/dcm_raw
#   - Use mapping.csv to determine which dcm files are garbage
#   - Throw away the garbage ones
#   - Copy everything else into _data/dicom/dcm

# Then we will convert the dcm files to png, etc. in another script.

python ./prepare_dcm_files.py