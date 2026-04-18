# Content Creator Pipeline

Converts a raw music video into a subtitle-scrolling video ready for upload.

---

## Pipeline Overview

```
original.mp4
    │
    ▼
1_vocal-seperator.py       →  vocals_<name>.mp4
    │
    ▼
2_mp4_pause_remover.py     →  ready4sub_<name>.mp4
    │
    ▼
[ElevenLabs API manually]  →  elevenlab.json
    │
    ▼
6_elevenlab2lyrics.py      →  lyrics.txt
    │
    ▼
31_subtitle_scroller.py    →  ready2up_<name>.mp4
```

---

## System Requirements

### OS
Ubuntu 20.04+ (or any Debian-based Linux)

### Python
Python 3.10

```bash
sudo apt install python3.10 python3.10-venv python3-pip
```

### System Packages
```bash
sudo apt update
sudo apt install -y ffmpeg fonts-noto
```

| Package      | Purpose                                         |
|--------------|-------------------------------------------------|
| `ffmpeg`     | Video processing across all steps               |
| `fonts-noto` | Noto Sans Bengali font for Bangla script rendering |

---

## Virtual Environment Setup

Run once from the project root:

```bash
# 1. Create venv (takes ~20 mins due to demucs/torch)
python3.10 -m venv venv310

# 2. Activate
source venv310/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install torch demucs torchcodec
pip install torchaudio==2.1.2
pip install "numpy<2"
pip install pydub
pip install openai
```

To activate in future sessions:
```bash
source start.sh
```

To deactivate:
```bash
source stop.sh
```

---

## Configuration

All file paths and names are controlled by `config.properties`.

Update these values before running:

```properties
# Input file
filelocation.original = ../git-ignore-files/1_input_files/
filename.original     = amar_sonar_bangla        ← change this
extention.original    = mp4
```

All generated file names are derived automatically from `filename.original`.

---

## Running the Pipeline

### Step 1 — Vocals + Pause Removal

```bash
cd 5_content_creator
source ../venv310/bin/activate     # if not already active
python 1_ready_for_subtitle.py
```

Runs in order:
1. `1_vocal-seperator.py` — extracts vocals using Demucs
2. `2_mp4_pause_remover.py` — removes long silences

Output: `../git-ignore-files/2_generated_files/ready4sub_<name>.mp4`

---

### Step 2 — Generate Lyrics (ElevenLabs)

Upload the vocals MP4 to [ElevenLabs](https://elevenlabs.io) and download the transcription JSON.

Save the file as:
```
../git-ignore-files/2_generated_files/elevenlab.json
```

---

### Step 3 — JSON to Lyrics Text

```bash
python ../4_subtitle-maker/6_elevenlab2lyrics.py
```

Output: `../git-ignore-files/2_generated_files/lyrics.txt`

---

### Step 4 — Subtitle Scroller Video

```bash
python ../4_subtitle-maker/31_subtitle_scroller.py
```

Output: `../git-ignore-files/3_final_files/ready2up_<name>.mp4`

---

## Generated Files

| File | Location | Description |
|------|----------|-------------|
| `vocals_<name>.mp4`   | `2_generated_files/` | Vocals only |
| `ready4sub_<name>.mp4` | `2_generated_files/` | Vocals with pauses removed |
| `elevenlab.json`      | `2_generated_files/` | ElevenLabs transcription |
| `lyrics.txt`          | `2_generated_files/` | Plain text lyrics |
| `ready2up_<name>.mp4` | `3_final_files/`     | Final video ready for upload |

---

## Troubleshooting

### Bangla text not rendering / wrong font size
```bash
sudo apt install fonts-noto
```

### ffmpeg not found
```bash
sudo apt install ffmpeg
ffmpeg -version
```

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