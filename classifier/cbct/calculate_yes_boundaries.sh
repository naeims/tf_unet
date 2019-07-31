#!/bin/bash

# Load results.csv
# Curve fit a single step function
# Output yes_boundaries.csv

python ./calculate_yes_boundaries.py > yes_boundaries.csv
