#!/bin/bash

STUDIES_DIR="../_data/jpg"
RESULT_FILE="results.csv"
RESULT_FILE_BACKUP="results_backup.csv"

# Delete result file
rm -rf $RESULT_FILE

# Create new result file
touch $RESULT_FILE
echo "study_id,slice_number,yesness" >> $RESULT_FILE

dirNames=$(ls $STUDIES_DIR/ | sort -V)
for dirName in $dirNames ; do
    dirPath=$STUDIES_DIR/$dirName
    dirStartTime=$SECONDS
    echo "Processing dir: $dirPath"

    lines=$(
    python label_all_images.py \
        --graph=./retrained_graph.pb \
        --labels=./retrained_labels.txt \
        --input_layer=Placeholder \
        --output_layer=final_result \
        --src_dir=$dirPath \
        2> /dev/null \
        | grep cbctyes
    )

    while read -r line; do
        fileName=$(echo "$line" | awk '{print $1}')
        val=$(echo "$line" | awk '{print $3}')
        sliceNumber=$(echo $fileName | sed -E "s/^[^_]+_(.+)\..+$/\1/")
        echo "$dirName,$sliceNumber,$val" >> $RESULT_FILE
    done <<< "$lines"

    dirElapsedTime=$(($SECONDS-$dirStartTime))
    echo "   >> Took $dirElapsedTime seconds."
done

cp $RESULT_FILE $RESULT_FILE_BACKUP
