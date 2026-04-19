# subtitle-maker

Converts a Bangla audio file and an SRT subtitle file into an MP4 video with
subtitles burned directly into the image.

```
input.mp3 + bangla_subtitles.srt  →  output.mp4
```

Subtitles are rendered in **yellow, bold, italic**, centered on screen.

---

## Requirements

### Operating System
Ubuntu 20.04+ (or any Debian-based Linux)

### Python
Python 3.10

```bash
sudo apt install python3.10 python3.10-venv python3-pip
```

### System packages
```bash
sudo apt update
sudo apt install -y ffmpeg fonts-noto
```

| Package      | Purpose                                      |
|--------------|----------------------------------------------|
| `ffmpeg`     | Renders video and burns subtitles into image |
| `fonts-noto` | Noto Sans Bengali font for Bangla script     |

> **Important:** Without `fonts-noto`, Bangla letters will not render correctly
> and the font size setting will be ignored.

### Python packages
None. This project uses the Python standard library only.

---

## Setup

```bash
# 1. Clone / navigate to project
cd subtitle-maker

# 2. Create virtual environment
python3.10 -m venv venv310

# 3. Activate virtual environment
source venv310/bin/activate

# 4. No pip install needed — stdlib only
```

To deactivate the virtual environment when done:
```bash
deactivate
```

---

## Input Files

| File                   | Description                              |
|------------------------|------------------------------------------|
| `input.mp3`            | Bangla audio file                        |
| `bangla_subtitles.srt` | SRT subtitle file with Bangla timestamps |

### SRT file format
```
1
00:00:00,160 --> 00:00:02,060
লাগে উড়া দুরা।

2
00:00:02,100 --> 00:00:03,700
লাগে উড়া দুরা ।
```

---

## Usage

```bash
python subtitle-maker.py input.mp3
```

### With a custom SRT file
```bash
python subtitle-maker.py input.mp3 --srt mysong.srt
```

### All options
```bash
python subtitle-maker.py --help
```

| Argument | Default                | Description              |
|----------|------------------------|--------------------------|
| `audio`  | `input.mp3`            | Input audio file         |
| `--srt`  | `bangla_subtitles.srt` | Input SRT subtitle file  |

---

## Output Files

| File         | Description                             |
|--------------|-----------------------------------------|
| `output.ass` | Intermediate styled subtitle file (ASS) |
| `output.mp4` | Final video with burned-in subtitles    |

The video is **1280×720** resolution with a black background.

---

## Subtitle Style

Defined in `write_ass()` inside `subtitle-maker.py`:

| Property   | Value              |
|------------|--------------------|
| Font       | Noto Sans Bengali  |
| Size       | 84pt               |
| Color      | Yellow             |
| Style      | Bold + Italic      |
| Position   | Center of screen   |
| Outline    | Black, 2px         |

To change these, edit the `Style:` line in the `write_ass()` function.

---

## Project Structure

```
subtitle-maker/
├── subtitle-maker.py       # Main script
├── bangla_subtitles.srt    # Input: Bangla subtitle file (gitignored)
├── input.mp3               # Input: audio file (gitignored)
├── output.ass              # Generated: styled subtitles (gitignored)
├── output.mp4              # Generated: final video (gitignored)
├── requirements.txt        # No pip packages — system deps noted here
├── .gitignore
├── venv.sh                 # Notes: venv setup commands
├── osenv.sh                # Notes: OS package install commands
├── stop.sh                 # Deactivate venv
└── subtitle-notes.md       # This file
```

---

## Troubleshooting

### Bangla letters not showing / font size not changing
Install the Noto fonts package:
```bash
sudo apt install fonts-noto
```

### ffmpeg not found
```bash
sudo apt install ffmpeg
ffmpeg -version   # verify install
```

### No sound in output video
Make sure `input.mp3` exists in the project folder before running.

### Empty subtitle blocks in SRT are ignored
SRT entries with no text (blank subtitle) are automatically skipped.

---

## How It Works

1. **Parse SRT** — reads `bangla_subtitles.srt`, extracts `(start, end, text)` for each entry
2. **Write ASS** — converts to ASS format with embedded font/color/position style
3. **Render video** — ffmpeg combines black background + audio + ASS subtitles into MP4

```
bangla_subtitles.srt
        │
        ▼
   parse_srt()
        │
        ▼
   write_ass()  →  output.ass
        │
        ▼
   make_video()  →  output.mp4  ←  input.mp3
```
