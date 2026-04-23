#!/bin/bash

# Script to move files from mountspace to 1_input_files

MOUNT_DIR="/myworkspace/mountspace"

# Define input and output directories
INPUT_DIR="$MOUNT_DIR"
OUTPUT_DIR="$MOUNT_DIR/1_input_files"

# Specify the input file name here
INPUT_FILE_NAME="k_basi_bajayre.mp4"  # Change this to your actual file name

# Move the specific input file
if [ -f "$INPUT_DIR/$INPUT_FILE_NAME" ]; then
    mv "$INPUT_DIR/$INPUT_FILE_NAME" "$OUTPUT_DIR/"
    echo "File $INPUT_FILE_NAME moved from $INPUT_DIR to $OUTPUT_DIR."
else
    echo "File $INPUT_FILE_NAME not found in $INPUT_DIR."
fi