from pydub import AudioSegment
import os
import sys

# --- Constants ---
DEFAULT_INPUT  = "input.wav"
DEFAULT_OUTPUT = "output.mp3"
EXPORT_FORMAT  = "mp3"


def wav_to_mp3(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    print(f"Converting {input_path} → {output_path}")
    audio = AudioSegment.from_wav(input_path)
    audio.export(output_path, format=EXPORT_FORMAT)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    wav_to_mp3(DEFAULT_INPUT, DEFAULT_OUTPUT)
