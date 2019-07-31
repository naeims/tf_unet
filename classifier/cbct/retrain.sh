#!/bin/bash

rm -rf /tmp/* ./retrained_graph.pb ./retrained_labels.txt

python retrain.py \
    --image_dir ../../_data/dicom/classifier_training/ \
    --how_many_training_steps 2000 \
    --output_graph=./retrained_graph.pb \
    --output_labels=./retrained_labels.txt \
    /