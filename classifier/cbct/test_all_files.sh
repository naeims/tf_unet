#!/bin/bash

STUDIES_DIR="../../_data/jpg"
RESULT_FILE="results.csv"

# Delete result file
rm -rf results.csv

dirNames=$(ls $STUDIES_DIR/ | sort -V)
for dirName in $dirNames ; do
    dirPath=$STUDIES_DIR/$dirName
    echo "Processing dir: $dirPath"
    fileNames=$(ls $dirPath | sort -V)
    for fileName in $fileNames ; do
        filePath=$dirPath/$fileName
        sliceNumber=$(
            echo $fileName | sed -E "s/^[^_]+_(.+)\..+$/\1/"
        )
        
        val=$(
        python label_image.py \
            --graph=./retrained_graph.pb \
            --labels=./retrained_labels.txt \
            --input_layer=Placeholder \
            --output_layer=final_result \
            --image=$filePath \
            2> /dev/null \
            | grep cbctyes \
            | awk '{print $2}'
        )
        echo "$dirName,$sliceNumber,$val" >> $RESULT_FILE
    done
done

cp results.csv results_backup.csv
