# Vocal Separator

Extracts vocals from a music video using Demucs (ML model) and outputs an MP4 with a black background.

```
original.mp4  →  vocals_<name>.mp4
```

---

## How It Works

1. Runs **Demucs** (`htdemucs` model) to separate vocals from the audio
2. Locates the generated `vocals.wav` in the temp folder
3. Converts `vocals.wav` to MP4 with a black background using ffmpeg

---

## Configuration

File paths are read from `../5_content_creator/config.properties`:

```properties
filelocation.original = ../git-ignore-files/1_input_files/
filename.original     = amar_sonar_bangla        ← change this
extention.original    = mp4

filelocation.vocals   = ../git-ignore-files/2_generated_files/
prefix.vocals         = vocals_
extention.vocals = mp4
```

---

## System Requirements

### OS
Ubuntu 20.04+ (or any Debian-based Linux)

### Python
Python 3.10

```bash
bash osenv.sh
```

---

## Virtual Environment Setup

Run once — takes ~20 minutes (downloads PyTorch + Demucs):

```bash
bash localenv.sh
```

---

## Run

```bash
source start.sh
python 1_vocal-seperator.py
```

---

## stop

```bash
source stop.sh

## Output

| File | Location |
|------|----------|
| `vocals_<name>.mp4` | `../git-ignore-files/2_generated_files/` |
| `demucs_temp/` | `../git-ignore-files/demucs_temp/` (intermediate, auto-cleaned) |

---

## Troubleshooting

### Demucs install fails
```bash
pip install torch==2.1.2
pip install torchaudio==2.1.2
pip install demucs
```

### numpy version conflict
```bash
pip install "numpy<2"
```

### python3.10 not found
```bash
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-distutils
```