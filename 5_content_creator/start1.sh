#!/bin/bash
# Activate the virtual environment.
# Also ensures all dependent project venvs are set up.


# Ensure 3_media-converters/4_mp42wav.py venv is ready
echo "Setting up 1_signals-process environment..."
cd ../3_media-converters
source venv310/bin/activate
python 4_mp42wav.py
source stop.sh
cd ../5_content_creator

# Ensure 1_signals-process/1d_wav_get_human.py venv is ready
echo "Setting up 1_signals-process environment..."
cd ../1_signals-process
source venv310/bin/activate
python 1d_wav_get_human.py 
source stop.sh
cd ../5_content_creator
