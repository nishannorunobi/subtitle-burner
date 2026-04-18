import subprocess
import os
import sys
import configparser

# Strategy: Demucs 4-stem separates vocals from other instruments (flute → "other" stem).
# Final mix = vocals (100%) + other (FLUTE_VOLUME) so voice is intact, flute is quiet.

DEMUCS_MODEL  = "htdemucs"
TEMP_DIR      = "../git-ignore-files/demucs_temp"
FLUTE_VOLUME  = 0.15   # 0.0 = silent, 1.0 = original — tune this to taste


def load_config(config_path="../5_content_creator/config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]


def run_demucs_4stem(input_path):
    os.makedirs(TEMP_DIR, exist_ok=True)
    print(f"Running Demucs 4-stem ({DEMUCS_MODEL}) on {input_path}...")
    subprocess.run([
        "demucs",
        "-n", DEMUCS_MODEL,
        "-o", TEMP_DIR,
        input_path,
    ], check=True)

    song_name = os.path.splitext(os.path.basename(input_path))[0]
    stem_dir  = os.path.join(TEMP_DIR, DEMUCS_MODEL, song_name)

    vocals_wav = os.path.join(stem_dir, "vocals.wav")
    other_wav  = os.path.join(stem_dir, "other.wav")

    for p in (vocals_wav, other_wav):
        if not os.path.exists(p):
            print(f"Error: expected stem not found: {p}")
            sys.exit(1)

    return vocals_wav, other_wav


def mix_vocals_with_reduced_other(vocals_wav, other_wav, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"Mixing: vocals 100% + other {int(FLUTE_VOLUME * 100)}%...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", vocals_wav,
        "-i", other_wav,
        "-filter_complex",
        f"[1]volume={FLUTE_VOLUME}[bg];[0][bg]amix=inputs=2:normalize=0",
        output_path,
    ], check=True)
    print(f"Saved: {output_path}")


def extract_human_voice(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    vocals_wav, other_wav = run_demucs_4stem(input_path)
    mix_vocals_with_reduced_other(vocals_wav, other_wav, output_path)


if __name__ == "__main__":
    _cfg = load_config()
    DEFAULT_INPUT  = _cfg["filelocation.processing"] + _cfg["filename.processing"] + "." + _cfg["extention.processing"]
    DEFAULT_OUTPUT = _cfg["filelocation.vocals"]     + _cfg["prefix.vocals"]       + "." + _cfg["extention.vocals"]
    extract_human_voice(DEFAULT_INPUT, DEFAULT_OUTPUT)