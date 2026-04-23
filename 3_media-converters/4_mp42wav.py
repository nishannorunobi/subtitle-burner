import subprocess
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "5_content_creator"
if str(CONFIG_DIR) not in sys.path:
    sys.path.insert(0, str(CONFIG_DIR))

from config import ORIGINAL_FILE_PATH, PROCESSING_FILE_PATH


def convert(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Converting {input_path} → {output_path}...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_path,
        "-vn",              # strip video
        "-acodec", "pcm_s16le",  # uncompressed WAV — best quality for audio processing
        "-ar", "44100",     # 44.1kHz sample rate
        "-ac", "2",         # stereo
        output_path,
    ], check=True)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    DEFAULT_INPUT = ORIGINAL_FILE_PATH
    DEFAULT_OUTPUT = PROCESSING_FILE_PATH
    convert(DEFAULT_INPUT, DEFAULT_OUTPUT)
