#!/bin/bash
source "$(dirname "${BASH_SOURCE[0]}")/../env.sh"
set -euo pipefail
# Activate (or create) the virtual environment and install dependencies on first run.

if [ ! -d "venv310" ]; then
    echo "venv310 not found. Creating environment and installing dependencies..."
    $PYTHON_BIN -m venv venv310
    source venv310/bin/activate
    source venv.sh
else
    source venv310/bin/activate
fi


