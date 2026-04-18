import subprocess
import os
import sys
import configparser

VIDEO_RESOLUTION = "320x240"
VIDEO_FPS        = "1"        # 1fps is enough for a static black frame
BG_COLOR         = "black"
VIDEO_CODEC      = "libx264"
VIDEO_CRF        = "51"       # maximum compression — black frame, quality is irrelevant
VIDEO_PRESET     = "ultrafast"
AUDIO_CODEC      = "aac"
AUDIO_BITRATE    = "128k"     # 128k is enough for voice


def load_config(config_path="../5_content_creator/config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]


def wav_to_mp4(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Converting {input_path} → {output_path}")
    print(f"  Video: {VIDEO_RESOLUTION} @ {VIDEO_FPS}fps CRF {VIDEO_CRF} (minimal black frame)")
    print(f"  Audio: {AUDIO_CODEC} {AUDIO_BITRATE}")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c={BG_COLOR}:s={VIDEO_RESOLUTION}:r={VIDEO_FPS}",
        "-i", input_path,
        "-map", "0:v",
        "-map", "1:a",
        "-shortest",
        "-c:v", VIDEO_CODEC,
        "-crf", VIDEO_CRF,
        "-preset", VIDEO_PRESET,
        "-c:a", AUDIO_CODEC,
        "-b:a", AUDIO_BITRATE,
        output_path,
    ], check=True)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Saved: {output_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    _cfg = load_config()
    DEFAULT_INPUT  = _cfg["filelocation.before_sub"] + _cfg["prefix.before_sub"] + "." + _cfg["extention.before_sub"]
    DEFAULT_OUTPUT = _cfg["filelocation.ready4sub"]  + _cfg["prefix.ready4sub"]  + "." + _cfg["extention.ready4sub"]
    wav_to_mp4(DEFAULT_INPUT, DEFAULT_OUTPUT)