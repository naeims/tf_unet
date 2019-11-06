#!/bin/bash

# Load results.csv
# Curve fit a single step function
# Output yes_boundaries.csv

FILE=yes_boundaries.csv

rm -rf $FILE
python ./calculate_yes_boundaries.py > $FILE
