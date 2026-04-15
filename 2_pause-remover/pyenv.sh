#!/bin/bash
# Create Python virtual environment and install dependencies.
# Run osenv.sh first if this is a fresh machine.

python3.10 -m venv venv310
source venv310/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Verify setup
python wav-pause-remover.py --help
