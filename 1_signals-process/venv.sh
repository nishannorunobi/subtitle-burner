#!/bin/bash
# Create virtual environment and install Python dependencies.
# Run osenv.sh first on a fresh machine.
# Note: takes ~20 minutes due to PyTorch + Demucs download.

pip install --upgrade pip
pip install torch demucs torchcodec
pip install torchaudio==2.1.2
pip install "numpy<2"
pip install silero-vad