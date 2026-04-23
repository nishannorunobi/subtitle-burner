import sys
import os
from pathlib import Path
import whisper


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "5_content_creator"
if str(CONFIG_DIR) not in sys.path:
    sys.path.insert(0, str(CONFIG_DIR))

from config import BEFORE_SUB_FILE_PATH, LYRICS_FILE_PATH

DEFAULT_INPUT_WAV = BEFORE_SUB_FILE_PATH
OUTPUT_LYRICS = LYRICS_FILE_PATH

# large-v3 = best quality, ~1.5 GB, downloads once to ~/.cache/whisper/
MODEL_NAME = "large-v3"


def transcribe(wav_path: str) -> str:
    print(f"  Loading Whisper model: {MODEL_NAME}  (downloads on first run ~1.5 GB)")
    model = whisper.load_model(MODEL_NAME)

    print(f"  Transcribing: {wav_path}  (this may take a few minutes...)")
    result = model.transcribe(
        wav_path,
        language="bn",          # Bengali
        task="transcribe",      # transcribe, not translate
        word_timestamps=False,
        verbose=False,
    )

    # Each segment becomes one lyric line; blank line between natural pauses
    lines = []
    prev_end = None
    for seg in result["segments"]:
        # Insert blank line if gap between segments is > 1.5 seconds (verse break)
        if prev_end is not None and (seg["start"] - prev_end) > 1.5:
            lines.append("")
        lines.append(seg["text"].strip())
        prev_end = seg["end"]

    return "\n".join(lines).strip()


def save_lyrics(lyrics: str, output_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(lyrics + "\n")
    print(f"  Saved: {output_path}")


def main():
    wav_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT_WAV

    if not os.path.exists(wav_path):
        print(f"Error: file not found: {wav_path}")
        sys.exit(1)

    print(f"Transcribing lyrics from: {wav_path}")
    lyrics = transcribe(wav_path)

    print("\n--- Transcribed Lyrics ---")
    print(lyrics)
    print("--------------------------\n")

    save_lyrics(lyrics, OUTPUT_LYRICS)


if __name__ == "__main__":
    main()
