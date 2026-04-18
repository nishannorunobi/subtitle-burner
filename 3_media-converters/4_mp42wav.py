import subprocess
import os
import sys
import configparser


def load_config(config_path="../5_content_creator/config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]


def convert(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Converting {input_path} → {output_path}...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_path,
        "-vn",              # strip video
        "-acodec", "pcm_s16le",  # uncompressed WAV — best quality for audio processing
        "-ar", "44100",     # 44.1kHz sample rate
        "-ac", "2",         # stereo
        output_path,
    ], check=True)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    _cfg = load_config()
    DEFAULT_INPUT  = _cfg["filelocation.original"]   + _cfg["filename.original"]   + "." + _cfg["extention.original"]
    DEFAULT_OUTPUT = _cfg["filelocation.processing"] + _cfg["filename.processing"] + "." + _cfg["extention.processing"]
    convert(DEFAULT_INPUT, DEFAULT_OUTPUT)