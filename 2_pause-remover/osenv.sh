#!/bin/bash
# OS-level dependencies for pause-remover
# Run once on a fresh machine before setting up the Python venv.

sudo apt update

# Python 3.10
sudo apt install -y python3.10 python3.10-venv python3-pip

# ffmpeg — audio backend used by pydub
sudo apt install -y ffmpeg
