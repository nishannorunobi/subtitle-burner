import subprocess
import tempfile
import re
import os
import sys
import configparser

def load_config(config_path="../5_content_creator/config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]

_cfg = load_config()

DEFAULT_INPUT  = _cfg["filelocation.vocals.vad"] + _cfg["prefix.vocals.vad"] + _cfg["filename.original"] + "." + _cfg["extention.vocals.vad"]
DEFAULT_OUTPUT = _cfg["filelocation.ready4sub"] + _cfg["prefix.ready4sub"] + _cfg["filename.original"] + "." + _cfg["extention.ready4sub"]
MAX_PAUSE_SEC      = 3.0
SILENCE_THRESH_DB  = -40
VIDEO_CODEC        = "libx264"
AUDIO_CODEC        = "aac"
AUDIO_BITRATE      = "192k"


def get_duration(input_path):
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_path,
    ], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def detect_long_silences(input_path):
    result = subprocess.run([
        "ffmpeg", "-i", input_path,
        "-af", f"silencedetect=noise={SILENCE_THRESH_DB}dB:d={MAX_PAUSE_SEC}",
        "-f", "null", "-",
    ], capture_output=True, text=True)

    output  = result.stderr
    starts  = [float(x) for x in re.findall(r"silence_start: (\d+\.?\d*)", output)]
    ends    = [float(x) for x in re.findall(r"silence_end: (\d+\.?\d*)", output)]
    return list(zip(starts, ends))


def get_keep_segments(silences, total_duration):
    segments = []
    prev_end = 0.0
    for silence_start, silence_end in silences:
        if silence_start > prev_end:
            segments.append((prev_end, silence_start))
        prev_end = silence_end
    if prev_end < total_duration:
        segments.append((prev_end, total_duration))
    return segments


def remove_long_pauses(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        print("Run 1c_vad_cleaner.py first.")
        sys.exit(1)

    print(f"Analysing {input_path}...")
    total_duration = get_duration(input_path)
    print(f"  Duration     : {total_duration:.1f}s")
    print(f"  Max pause    : {MAX_PAUSE_SEC}s")

    silences = detect_long_silences(input_path)
    print(f"  Long pauses  : {len(silences)} found")

    if not silences:
        print("No long pauses found. Copying input to output...")
        subprocess.run(["ffmpeg", "-y", "-i", input_path,
                        "-c", "copy", output_path], check=True)
        print(f"Saved: {output_path}")
        return

    segments = get_keep_segments(silences, total_duration)
    print(f"  Segments kept: {len(segments)}")

    with tempfile.TemporaryDirectory() as tmp:
        concat_list = os.path.join(tmp, "concat.txt")
        segment_files = []

        for i, (start, end) in enumerate(segments):
            seg_file = os.path.join(tmp, f"seg_{i:04d}.mp4")
            subprocess.run([
                "ffmpeg", "-y",
                "-i", input_path,
                "-ss", str(start),
                "-to", str(end),
                "-c:v", VIDEO_CODEC,
                "-c:a", AUDIO_CODEC,
                "-b:a", AUDIO_BITRATE,
                seg_file,
            ], check=True, capture_output=True)
            segment_files.append(seg_file)

        with open(concat_list, "w") as f:
            for seg in segment_files:
                f.write(f"file '{seg}'\n")

        print(f"Merging segments → {output_path}...")
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_list,
            "-c", "copy",
            output_path,
        ], check=True)

    removed = total_duration - get_duration(output_path)
    print(f"  Removed      : {removed:.1f}s of silence")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    remove_long_pauses(DEFAULT_INPUT, DEFAULT_OUTPUT)