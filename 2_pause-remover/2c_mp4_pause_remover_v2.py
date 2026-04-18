import subprocess
import tempfile
import re
import os
import sys
import configparser

# v2 — works on audio only during processing to avoid video timing drift.
# Steps: extract audio → detect silences → remove silences (audio only) → rebuild mp4.

MAX_PAUSE_SEC     = 3.0    # remove pauses longer than this (seconds)
SILENCE_THRESH_DB = -40    # volume below which is considered silence
VIDEO_RESOLUTION  = "1280x720"
VIDEO_FPS         = "25"
BG_COLOR          = "black"
VIDEO_CODEC       = "libx264"
AUDIO_CODEC       = "aac"
AUDIO_BITRATE     = "192k"


def load_config(config_path="../5_content_creator/config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]


def get_duration(path):
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path,
    ], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def extract_audio(input_mp4, output_wav):
    subprocess.run([
        "ffmpeg", "-y", "-i", input_mp4,
        "-vn", "-ac", "2", "-ar", "44100",
        output_wav,
    ], check=True, capture_output=True)


def detect_long_silences(wav_path):
    result = subprocess.run([
        "ffmpeg", "-i", wav_path,
        "-af", f"silencedetect=noise={SILENCE_THRESH_DB}dB:d={MAX_PAUSE_SEC}",
        "-f", "null", "-",
    ], capture_output=True, text=True)

    output = result.stderr
    starts = [float(x) for x in re.findall(r"silence_start: (\d+\.?\d*)", output)]
    ends   = [float(x) for x in re.findall(r"silence_end: (\d+\.?\d*)", output)]
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


def remove_silence_from_audio(wav_path, segments, output_wav, tmp):
    if not segments:
        return wav_path

    seg_files = []
    concat_list = os.path.join(tmp, "concat.txt")

    for i, (start, end) in enumerate(segments):
        seg_file = os.path.join(tmp, f"seg_{i:04d}.wav")
        subprocess.run([
            "ffmpeg", "-y", "-i", wav_path,
            "-ss", str(start), "-to", str(end),
            seg_file,
        ], check=True, capture_output=True)
        seg_files.append(seg_file)

    with open(concat_list, "w") as f:
        for s in seg_files:
            f.write(f"file '{s}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        output_wav,
    ], check=True, capture_output=True)

    return output_wav


def build_mp4(clean_wav, output_mp4):
    os.makedirs(os.path.dirname(output_mp4), exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c={BG_COLOR}:s={VIDEO_RESOLUTION}:r={VIDEO_FPS}",
        "-i", clean_wav,
        "-map", "0:v", "-map", "1:a",
        "-shortest",
        "-c:v", VIDEO_CODEC,
        "-c:a", AUDIO_CODEC,
        "-b:a", AUDIO_BITRATE,
        output_mp4,
    ], check=True)


def remove_long_pauses(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmp:
        raw_wav   = os.path.join(tmp, "audio_raw.wav")
        clean_wav = os.path.join(tmp, "audio_clean.wav")

        print(f"Extracting audio from {input_path}...")
        extract_audio(input_path, raw_wav)

        total_duration = get_duration(raw_wav)
        print(f"  Duration     : {total_duration:.1f}s")
        print(f"  Max pause    : {MAX_PAUSE_SEC}s")

        silences = detect_long_silences(raw_wav)
        print(f"  Long pauses  : {len(silences)} found")

        if not silences:
            print("No long pauses found. Copying input to output...")
            subprocess.run(["ffmpeg", "-y", "-i", input_path, "-c", "copy", output_path], check=True)
            print(f"Saved: {output_path}")
            return

        segments = get_keep_segments(silences, total_duration)
        print(f"  Segments kept: {len(segments)}")

        print("Removing silences from audio...")
        remove_silence_from_audio(raw_wav, segments, clean_wav, tmp)

        clean_duration = get_duration(clean_wav)
        removed = total_duration - clean_duration
        print(f"  Removed      : {removed:.1f}s of silence")

        print(f"Building output video: {output_path}...")
        build_mp4(clean_wav, output_path)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    _cfg = load_config()
    DEFAULT_INPUT  = _cfg["filelocation.vocals"] + _cfg["prefix.vocals"] + _cfg["filename.original"] + "." + _cfg["extention.vocals"]
    DEFAULT_OUTPUT = _cfg["filelocation.ready4sub"] + _cfg["prefix.ready4sub"] + _cfg["filename.original"] + "." + _cfg["extention.ready4sub"]
    remove_long_pauses(DEFAULT_INPUT, DEFAULT_OUTPUT)