#!/bin/bash
# Activate the virtual environment.
# Also ensures all dependent project venvs are set up.

set -euo pipefail

# step 1: 3_media-converters/4_mp42wav.py venv is ready
echo "Step 1: Setting up 3_media-converters environment..."
cd ../3_media-converters
source start.sh
python 4_mp42wav.py
source stop.sh
cd ../5_content_creator

# step 2: 1_signals-process/1d_wav_get_human.py venv is ready
# This step runs only if step 1 succeeded.
echo "Step 2: Setting up 1_signals-process environment..."
cd ../1_signals-process
source start.sh
python 1d_wav_get_human.py 
source stop.sh
cd ../5_content_creator
