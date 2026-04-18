#!/bin/bash
# Activate the virtual environment.
# Also ensures all dependent project venvs are set up.


# Ensure 1_signals-process venv is ready
echo "Setting up 1_signals-process environment..."
cd ../1_signals-process
source start.sh
source stop.sh
cd ../5_content_creator

# Ensure 2_pause-remover venv is ready
echo "Setting up 2_pause-remover environment..."
cd ../2_pause-remover
source start.sh
source stop.sh
cd ../5_content_creator

