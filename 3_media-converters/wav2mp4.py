import subprocess
import argparse
import os
import sys

# --- Constants ---
DEFAULT_INPUT    = "../2_pause-remover/no-pause.wav"
DEFAULT_OUTPUT   = "no-pause.mp4"
VIDEO_RESOLUTION = "1280x720"
VIDEO_FPS        = "25"
BG_COLOR         = "black"
VIDEO_CODEC      = "libx264"
AUDIO_CODEC      = "aac"
AUDIO_BITRATE    = "192k"


def wav_to_mp4(input_path, output_path):
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c={BG_COLOR}:s={VIDEO_RESOLUTION}:r={VIDEO_FPS}",
        "-i", input_path,
        "-map", "0:v",
        "-map", "1:a",
        "-shortest",
        "-c:v", VIDEO_CODEC,
        "-c:a", AUDIO_CODEC,
        "-b:a", AUDIO_BITRATE,
        output_path,
    ]
    subprocess.run(cmd, check=True)
    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert WAV audio to MP4 video with black background."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=DEFAULT_INPUT,
        help=f"Input WAV file (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output MP4 file (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: input file not found: {args.input}")
        sys.exit(1)

    print(f"Converting {args.input} → {args.output}")
    wav_to_mp4(args.input, args.output)


if __name__ == "__main__":
    main()
