#!/bin/bash
# Activate the virtual environment.
# Also ensures all dependent project venvs are set up.


# Ensure 2_pause-remover venv is ready
echo "Setting up 2_pause-remover environment..."
cd ../2_pause-remover
source venv310/bin/activate

python 2f_time_cutter.py
#python 2a_wav_pause_remover.py
#python 2e_wav_compressor.py

source stop.sh
cd ../5_content_creator
