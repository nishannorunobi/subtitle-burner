#!/bin/bash
# OS-level dependencies — run once on a fresh machine.

apt update
apt install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt update
apt install -y python3.10 python3.10-venv python3.10-distutils python3-pip
sudo apt install -y ffmpeg fonts-noto

