# Python Study Project

## Docker Setup

### First time — build the image
```bash
docker compose build
```

### Run the container
```bash
docker compose run --rm study
```
Drops you into a shell at `/workspace/5_content_creator` with API keys loaded from `git-ignore-files/osenv.sh`.

### Rebuild after Dockerfile changes
```bash
docker compose build --no-cache
```

### Remove unused images
```bash
docker image prune
```

---

## Project Structure

| Project | Description |
|---------|-------------|
| `1_signals-process/` | Extract vocals from audio |
| `2_pause-remover/` | Remove silence/pauses from wav |
| `3_media-converters/` | Convert mp4 → wav and other formats |
| `4_subtitle-burner/` | Burn scrolling subtitles into video |
| `5_content_creator/` | **Main entry point** — orchestrates all scripts |
| `6_lyrics-generator/` | Generate Bengali lyrics via Gemini / Claude / Whisper |

---

## Running Scripts (from inside container)

All scripts are run from `5_content_creator/`:

```bash
bash start1.sh   # mp4 → wav → vocal extraction
bash start2.sh   # pause removal
bash start3.sh   # subtitle burning
```

---

## Setting Up a Project's Virtual Environment (first time per project)

```bash
cd ../6_lyrics-generator       # or any other project
python -m venv venv310
source venv310/bin/activate
bash venv.sh                   # installs project-specific packages
```

---

## API Keys

Keys are stored in `git-ignore-files/osenv.sh` (git-ignored).
They are automatically loaded when the container starts.

To add or update a key, edit `git-ignore-files/osenv.sh`:
```bash
export GEMINI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
```
