1. The Strategy: Masking the SpectrogramMost ML models don't look at the raw array of PCM integers directly. Instead, they convert that 5-second array into a Spectrogram—a visual "heat map" of frequencies over time.The ML model (usually a U-Net or Transformer architecture) acts like a highly advanced highlighter. It looks at the complex "mess" of the full song's spectrogram and predicts a Vocal Mask.The Mask: A map of which "pixels" in the spectrogram belong to a human voice.The Extraction: The model multiplies the original spectrogram by this mask, effectively "muting" everything except the human voice.

2. Popular ML Tools to Use
Demucs (v4)Meta (Facebook)High Quality. Currently the industry gold standard for clean vocals with minimal "watery" artifacts.

# For Ubuntu/Debian/Mint:
sudo apt update && sudo apt install ffmpeg python3-pip -y

# For Fedora:
sudo dnf install ffmpeg python3-pip -y

# For Arch:
sudo pacman -S ffmpeg python-pip

# Install demucs
pip install demucs
pip install torchcodec

# Run the program
python transcriber.py


# Troubleshoots
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

sudo apt install python3.10 python3.10-venv python3.10-distutils

python3.10 -m venv venv310
source venv310/bin/activate

pip install --upgrade pip
pip install torch demucs torchcodec

pip uninstall torchcodec -y
pip install soundfile

pip install torchaudio==2.1.2
pip install "numpy<2"
