#!/bin/bash
# Create and activate the Python virtual environment.
# Run osenv.sh first if this is a fresh machine.

python3.10 -m venv venv310
source venv310/bin/activate

# No pip packages required — stdlib only.
# Verify setup:
python subtitle-maker.py --help
