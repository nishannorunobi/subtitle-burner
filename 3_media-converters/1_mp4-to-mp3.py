
import subprocess
import argparse
import os
import sys

# --- Constants ---
DEFAULT_INPUT  = "../git-ignore-files/0_0_0_original_music.mp4"
DEFAULT_OUTPUT = "../git-ignore-files/3_1_1_mp3music.mp3"
AUDIO_CODEC    = "libmp3lame"
AUDIO_BITRATE  = "192k"


def mp4_to_mp3(input_path, output_path):
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vn",
        "-c:a", AUDIO_CODEC,
        "-b:a", AUDIO_BITRATE,
        output_path,
    ]
    subprocess.run(cmd, check=True)
    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract audio from MP4 and save as MP3."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=DEFAULT_INPUT,
        help=f"Input MP4 file (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output MP3 file (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: input file not found: {args.input}")
        sys.exit(1)

    print(f"Converting {args.input} → {args.output}")
    mp4_to_mp3(args.input, args.output)


if __name__ == "__main__":
    main()
