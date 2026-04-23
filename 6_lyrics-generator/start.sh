#!/bin/bash
source "$(dirname "${BASH_SOURCE[0]}")/../env.sh"
# Activate the virtual environment.

if [ ! -d "venv310" ]; then
    echo "venv310 not found. Running venv.sh to set up the environment..."
    $PYTHON_BIN -m venv venv310
    source venv310/bin/activate
    source venv.sh
else
    source venv310/bin/activate
fi
