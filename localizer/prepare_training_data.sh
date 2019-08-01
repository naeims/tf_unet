#!/bin/bash

# Load mapping.csv
# Make dir data/training
# For every study that is in the training set
#    Copy each file from _data/png into _data/localizer_training, e.g. 10_49.png
#    Copy labels from _data/raw_labels into _data/localizer_training, e.g. 10_49_mask.png
#       --- convert greyscale+red to black+white
#       --- for every non-black label, put a copy in data/labels

python ./prepare_training_data.py
