#!/bin/bash
#FILES=_data/128x128_patches
FILES=_data/full_size
#NEGATIVE_FILES=_data/128x128_patches_negative

TARGET_DIR=cbct/data/training

# delete old images
rm $TARGET_DIR/*.png

# copy images
cp $FILES/image/*.png $TARGET_DIR

# copy masks
for f in $FILES/label/*.png
do
	source_filename=$(basename -- "$f")
	mask_filename="${source_filename%.*}_mask.png"
	cp $f $TARGET_DIR/$mask_filename
done

if [ -n "$NEGATIVE_FILES" ]; then
    for f in $NEGATIVE_FILES/image/*.png
    do
        source_filename=$(basename -- "$f")
        image_filename="n${source_filename%.*}.png"
        mask_filename="n${source_filename%.*}_mask.png"
        cp $f $TARGET_DIR/$image_filename
        cp $NEGATIVE_FILES/label/0.png $TARGET_DIR/$mask_filename
    done
else
  echo "No negative files."
fi
