from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import argparse
import os
import sys

# --- Constants ---
DEFAULT_INPUT      = "../1_signals-process/separated_results/htdemucs/mymusic/vocals.wav"
DEFAULT_OUTPUT     = "no-pause.wav"
MAX_PAUSE_MS       = 2000
SILENCE_THRESH_DB  = -40
SEEK_STEP_MS       = 10
EXPORT_FORMAT      = "wav"


def remove_long_pauses(audio, max_pause_ms, silence_thresh_db):
    """
    Return audio with all pauses longer than max_pause_ms removed.
    Pauses shorter than or equal to max_pause_ms are kept as-is.

    How it works:
      detect_nonsilent() splits the audio on any silence >= max_pause_ms.
      The resulting chunks already contain all short pauses within them.
      Concatenating the chunks discards only the long pauses between them.
    """
    chunks = detect_nonsilent(
        audio,
        min_silence_len=max_pause_ms,
        silence_thresh=silence_thresh_db,
        seek_step=SEEK_STEP_MS,
    )

    if not chunks:
        print("Warning: no speech detected. Try lowering --silence-thresh (e.g. --silence-thresh -50).")
        return audio

    result = AudioSegment.empty()
    for start, end in chunks:
        result += audio[start:end]

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Remove pauses longer than a threshold from a WAV file."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=DEFAULT_INPUT,
        help=f"Input WAV file (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default=DEFAULT_OUTPUT,
        help=f"Output WAV file (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--max-pause",
        type=int,
        default=MAX_PAUSE_MS,
        help=f"Pauses longer than this (ms) are removed. Default: {MAX_PAUSE_MS}.",
    )
    parser.add_argument(
        "--silence-thresh",
        type=int,
        default=SILENCE_THRESH_DB,
        help=f"Volume level (dBFS) below which audio is considered silence. "
             f"Default: {SILENCE_THRESH_DB}. Lower = stricter (e.g. -50 for quiet recordings).",
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: input file not found: {args.input}")
        sys.exit(1)

    print(f"Loading {args.input}...")
    audio = AudioSegment.from_wav(args.input)
    original_duration = len(audio) / 1000
    print(f"  Duration     : {original_duration:.1f}s")
    print(f"  Max pause    : {args.max_pause}ms")
    print(f"  Silence level: {args.silence_thresh} dBFS")

    print("Removing long pauses...")
    result = remove_long_pauses(audio, args.max_pause, args.silence_thresh)

    removed = original_duration - len(result) / 1000
    print(f"  Removed      : {removed:.1f}s of silence")
    print(f"  Output length: {len(result)/1000:.1f}s")

    print(f"Exporting {args.output}...")
    result.export(args.output, format=EXPORT_FORMAT)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
