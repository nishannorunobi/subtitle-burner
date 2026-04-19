#!/bin/bash
# Install Python dependencies.
# Run osenv.sh first on a fresh machine.

pip install --upgrade pip
pip install anthropic
pip install google-genai

# Whisper — offline transcription (best quality, free)
pip install openai-whisper
# PyTorch CPU-only (lighter install, still works — remove --index-url line for GPU)
pip install torch --index-url https://download.pytorch.org/whl/cpu
