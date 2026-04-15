from openai import OpenAI
import argparse
import os
import sys

# --- Constants ---
WHISPER_MODEL    = "whisper-1"
RESPONSE_FORMAT  = "srt"
OUTPUT_EXTENSION = ".srt"
DEFAULT_INPUT    = "input.mp3"
API_KEY_ENV_VAR  = "OPENAI_API_KEY"


def audio_to_srt(audio_path, output_path):
    api_key = os.environ.get(API_KEY_ENV_VAR)
    if not api_key:
        print(f"Error: {API_KEY_ENV_VAR} environment variable is not set.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    print(f"Uploading: {audio_path}")
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=WHISPER_MODEL,
            file=audio_file,
            response_format=RESPONSE_FORMAT,
        )

    srt_content = response if isinstance(response, str) else response.text

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert audio to SRT subtitle file using OpenAI Whisper."
    )
    parser.add_argument(
        "audio",
        nargs="?",
        default=DEFAULT_INPUT,
        help=f"Input audio file (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output SRT file (default: same name as audio, e.g. input.mp3 → input.srt)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"Error: audio file not found: {args.audio}")
        sys.exit(1)

    output = args.output or os.path.splitext(args.audio)[0] + OUTPUT_EXTENSION
    audio_to_srt(args.audio, output)


if __name__ == "__main__":
    main()
