import subprocess
import os

# --- Constants ---
DEFAULT_INPUT  = "../git-ignore-files/mymusic.mp4"
DEMUCS_MODEL   = "no-vocals"
STEM_TYPE      = "vocals"
OUTPUT_DIR     = "../git-ignore-files/"


def separate_vocals(audio_file):
    current_dir = os.getcwd()
    input_path  = os.path.join(current_dir, audio_file)
    output_path = os.path.join(current_dir, OUTPUT_DIR)

    if not os.path.exists(input_path):
        print(f"Error: {audio_file} not found in {current_dir}")
        return

    command = [
        "demucs",
        "-n", DEMUCS_MODEL,
        "--two-stems", STEM_TYPE,
        "-o", output_path,
        input_path,
    ]

    print(f"Reading MP3 and extracting vocals...")
    subprocess.run(command, check=True)

    song_name = os.path.splitext(audio_file)[0]
    print(f"Finished! Your isolated voice is at: {output_path}/{DEMUCS_MODEL}/{song_name}/{STEM_TYPE}.wav")


if __name__ == "__main__":
    separate_vocals(DEFAULT_INPUT)
