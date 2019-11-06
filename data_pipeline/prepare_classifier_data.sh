#!/bin/bash

# For all directories in _data/png
#   - Use mapping.csv to determine which png files are C3/C4 and which are not
#   - Move all C3/C4 files into _data/classifier_training/cbctyes
#   - Move all non C3/C4 files into _data/classifier_training/cbctno

# Then, separate both categories into training & test sets and copy them to TBD.
# Then we run classifier training to create the model.

python ./prepare_classifier_data.py