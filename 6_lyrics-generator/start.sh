#!/bin/bash
# Activate the virtual environment.

if [ ! -d "venv310" ]; then
    echo "venv310 not found. Running venv.sh to set up the environment..."
    python3.10 -m venv venv310
    source venv310/bin/activate
    bash venv.sh
else
    source venv310/bin/activate
fi
