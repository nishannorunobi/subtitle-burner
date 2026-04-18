#!/bin/bash
# OS-level dependencies — run once on a fresh machine.

sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-distutils python3-pip
sudo apt install -y ffmpeg