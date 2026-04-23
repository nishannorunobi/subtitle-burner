#!/bin/bash
# Activate the virtual environment.
# Also ensures all dependent project venvs are set up.


# Ensure 4_subtitle-maker venv is ready
echo "Setting up 4_subtitle-maker  environment..."
cd ../4_lyrics-burner 
source venv310/bin/activate
python 32_subtitle_scroller.py
source stop.sh
cd ../5_content_creator
