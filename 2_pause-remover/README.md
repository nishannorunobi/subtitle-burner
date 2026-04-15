# pause-remover

Removes long pauses (silences) from a WAV audio file.
Pauses **longer than 2 seconds** are removed. Pauses **2 seconds or shorter** are kept as-is.

```
input.wav  →  wav-pause-remover.py  →  output.wav
```

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
sudo apt install -y ffmpeg
```

| Package  | Purpose                                  |
|----------|------------------------------------------|
| `ffmpeg` | Audio backend used by pydub for decoding |

### Python packages
```
pydub==0.25.1
```

---

## Setup

```bash
# Step 1 — install OS dependencies (run once on a fresh machine)
bash osenv.sh

# Step 2 — create virtual environment
python3.10 -m venv venv310

# Step 3 — activate virtual environment
source venv310/bin/activate

# Step 4 — install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Step 5 — run the script
python wav-pause-remover.py input.wav
```

To deactivate the virtual environment when done:
```bash
deactivate
```

---

## Input / Output

| File         | Description                  |
|--------------|------------------------------|
| `input.wav`  | Source WAV audio file        |
| `output.wav` | Cleaned WAV with long pauses removed |

---

## Usage

### Default (removes pauses longer than 2 seconds)
```bash
python wav-pause-remover.py input.wav
```

### Custom output filename
```bash
python wav-pause-remover.py input.wav output-clean.wav
```

### Custom pause threshold
```bash
# Remove pauses longer than 3 seconds instead of 2
python wav-pause-remover.py input.wav --max-pause 3000
```

### Adjust silence detection sensitivity
```bash
# Use -50 dBFS for quiet recordings (default is -40)
python wav-pause-remover.py input.wav --silence-thresh -50
```

### All options
```bash
python wav-pause-remover.py --help
```

| Argument           | Default      | Description                                                  |
|--------------------|--------------|--------------------------------------------------------------|
| `input`            | `input.wav`  | Input WAV file                                               |
| `output`           | `output.wav` | Output WAV file                                              |
| `--max-pause`      | `2000`       | Pauses longer than this (ms) are removed                     |
| `--silence-thresh` | `-40`        | Volume below which audio is silence (dBFS). Lower = stricter |

---

## Example Output

```
Loading input.wav...
  Duration     : 120.4s
  Max pause    : 2000ms
  Silence level: -40 dBFS
Removing long pauses...
  Removed      : 22.1s of silence
  Output length: 98.3s
Saved: output.wav
```

---

## Project Structure

```
pause-remover/
├── wav-pause-remover.py   # Main script
├── input.wav              # Input audio file (gitignored)
├── output.wav             # Output audio file (gitignored)
├── requirements.txt       # Python dependencies
├── osenv.sh               # OS package install script
├── pyenv.sh               # Python venv setup script
├── stop.sh                # Deactivate venv
├── .gitignore
└── README.md              # This file
```

---

## How It Works

1. **Load** — reads `input.wav` using pydub
2. **Detect** — `detect_nonsilent()` finds all speech segments separated by silences ≥ `max_pause`
3. **Concatenate** — speech chunks are joined together, dropping the long silences between them
4. **Export** — writes the result to `output.wav`

Short pauses (< `max_pause`) are preserved naturally because they fall **within** speech chunks,
not between them.

```
input :  [speech]---[speech]--------[speech]--[speech]
                 ^^^            ^^^^^^^^^^^^
                 kept (≤2s)     removed (>2s)

output:  [speech]---[speech][speech]--[speech]
```

---

## Troubleshooting

### No speech detected / output is silent
The silence threshold may be too strict for your recording. Try lowering it:
```bash
python wav-pause-remover.py input.wav --silence-thresh -50
```

### pydub not found
Make sure you activated the virtual environment first:
```bash
source venv310/bin/activate
```

### ffmpeg not found error
```bash
sudo apt install ffmpeg
ffmpeg -version   # verify
```

### Output is same length as input (no pauses removed)
The audio may not have any pauses longer than `--max-pause`. Try reducing the threshold:
```bash
python wav-pause-remover.py input.wav --max-pause 1000
```
