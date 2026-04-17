import subprocess
import os
import sys

# --- Constants ---
DEFAULT_INPUT    = "../git-ignore-files/0_0_0_original_music.mp4"
DEFAULT_OUTPUT   = "../git-ignore-files/1_1_1_vocals.mp4"
DEMUCS_MODEL     = "htdemucs"
STEM_TYPE        = "vocals"
TEMP_DIR         = "../git-ignore-files/demucs_temp"
VIDEO_RESOLUTION = "1280x720"
VIDEO_FPS        = "25"
BG_COLOR         = "black"
VIDEO_CODEC      = "libx264"
AUDIO_CODEC      = "aac"
AUDIO_BITRATE    = "192k"


def extract_vocals(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    os.makedirs(TEMP_DIR, exist_ok=True)

    # Step 1 — separate vocals using demucs
    print(f"Extracting vocals from {input_path}...")
    subprocess.run([
        "demucs",
        "-n", DEMUCS_MODEL,
        "--two-stems", STEM_TYPE,
        "-o", TEMP_DIR,
        input_path,
    ], check=True)

    # Step 2 — locate the vocals.wav demucs created
    song_name  = os.path.splitext(os.path.basename(input_path))[0]
    vocals_wav = os.path.join(TEMP_DIR, DEMUCS_MODEL, song_name, f"{STEM_TYPE}.wav")

    if not os.path.exists(vocals_wav):
        print(f"Error: vocals file not found at {vocals_wav}")
        sys.exit(1)

    # Step 3 — convert vocals.wav to mp4 (black background video)
    print(f"Converting vocals to {output_path}...")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c={BG_COLOR}:s={VIDEO_RESOLUTION}:r={VIDEO_FPS}",
        "-i", vocals_wav,
        "-map", "0:v",
        "-map", "1:a",
        "-shortest",
        "-c:v", VIDEO_CODEC,
        "-c:a", AUDIO_CODEC,
        "-b:a", AUDIO_BITRATE,
        output_path,
    ], check=True)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    extract_vocals(DEFAULT_INPUT, DEFAULT_OUTPUT)
