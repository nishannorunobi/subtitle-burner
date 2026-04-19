import subprocess
import os
import sys
import configparser


def load_config(config_path="../5_content_creator/config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]

_cfg = load_config()

DEFAULT_INPUT_WAV  = _cfg["filelocation.before_sub"] + _cfg["prefix.before_sub"] + "." + _cfg["extention.before_sub"]
DEFAULT_LYRICS_TXT = _cfg["filelocation.lyrics"]     + _cfg["prefix.lyrics"]     + "." + _cfg["extention.lyrics"]
DEFAULT_OUTPUT_MP4 = _cfg["filelocation.ready2up"]   + _cfg["prefix.ready2up"]   + _cfg["filename.original"] + "." + _cfg["extention.ready2up"]
DEFAULT_OUTPUT_ASS = "scroll32.ass"

# Video
VIDEO_CODEC   = "libx264"
VIDEO_CRF     = "23"        # higher = smaller file; 18=sharp text, 23=default, 28=blurry text
AUDIO_CODEC   = "aac"
AUDIO_BITRATE = "192k"
FRAME_RATE    = "30"

# Subtitle style
FONT_NAME     = "Noto Sans Bengali"
FONT_SIZE     = "60"
FONT_COLOR    = "&H0000FFFF"   # yellow
OUTLINE_COLOR = "&H00000000"   # black
BACK_COLOR    = "&H80000000"
BOLD          = "-1"
ITALIC        = "-1"
OUTLINE_WIDTH = "2"

# Scroll layout
PLAY_RES_X  = 1280
PLAY_RES_Y  = 720
LINE_HEIGHT = 85   # approx pixel height per line at FONT_SIZE 60 (Bengali italic needs extra space)


def get_duration(input_path):
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_path,
    ], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def parse_lyrics(lyrics_path):
    with open(lyrics_path, "r", encoding="utf-8-sig") as f:
        raw = f.read().replace("\r\n", "\n").replace("\r", "\n")
    return [line.strip() for line in raw.splitlines() if line.strip()]


def fmt_ass_time(t):
    t  = max(0.0, t)
    h  = int(t // 3600)
    m  = int((t % 3600) // 60)
    s  = int(t % 60)
    cs = int(round((t - int(t)) * 100))
    return f"{h}:{m:02}:{s:02}.{cs:02}"


def write_scroll_ass(lines, ass_path, total_duration):
    n             = len(lines)
    time_per_line = total_duration / n
    speed         = LINE_HEIGHT / time_per_line   # pixels per second

    half_traverse = (PLAY_RES_Y / 2 + LINE_HEIGHT) / speed

    cx             = PLAY_RES_X // 2
    y_enter_screen = PLAY_RES_Y + LINE_HEIGHT   # below screen
    y_exit_screen  = -LINE_HEIGHT               # above screen

    header = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        f"PlayResX: {PLAY_RES_X}\n"
        f"PlayResY: {PLAY_RES_Y}\n"
        "ScaledBorderAndShadow: yes\n"
        "\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Default,{FONT_NAME},{FONT_SIZE},"
        f"{FONT_COLOR},&H000000FF,{OUTLINE_COLOR},{BACK_COLOR},"
        f"{BOLD},{ITALIC},0,0,100,100,0,0,1,{OUTLINE_WIDTH},0,5,10,10,10,1\n"
        "\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header)
        for i, line in enumerate(lines):
            t_center = (i + 0.5) * time_per_line
            t_enter  = t_center - half_traverse
            t_exit   = t_center + half_traverse

            if t_enter < 0:
                y1 = y_enter_screen + t_enter * speed
                t1 = 0.0
            else:
                y1 = y_enter_screen
                t1 = t_enter

            move_tag = f"{{\\move({cx},{int(y1)},{cx},{int(y_exit_screen)})}}"
            f.write(
                f"Dialogue: 0,{fmt_ass_time(t1)},"
                f"{fmt_ass_time(t_exit)},Default,,0,0,0,,{move_tag}{line}\n"
            )


def make_video(input_wav, ass_path, output_path):
    abs_ass = os.path.abspath(ass_path).replace("\\", "/").replace(":", "\\:")
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c=black:s={PLAY_RES_X}x{PLAY_RES_Y}:r={FRAME_RATE}",
        "-i", os.path.abspath(input_wav),
        "-shortest",
        "-vf", f"ass={abs_ass}",
        "-c:v", VIDEO_CODEC,
        "-crf", VIDEO_CRF,
        "-c:a", AUDIO_CODEC,
        "-b:a", AUDIO_BITRATE,
        os.path.abspath(output_path),
    ]
    subprocess.run(cmd, check=True)
    print(f"Saved: {output_path}")


def main():
    for path in (DEFAULT_INPUT_WAV, DEFAULT_LYRICS_TXT):
        if not os.path.exists(path):
            print(f"Error: file not found: {path}")
            sys.exit(1)

    print(f"Parsing {DEFAULT_LYRICS_TXT}...")
    lines = parse_lyrics(DEFAULT_LYRICS_TXT)
    print(f"  {len(lines)} lyric lines loaded")

    print(f"Getting duration of {DEFAULT_INPUT_WAV}...")
    duration = get_duration(DEFAULT_INPUT_WAV)
    print(f"  Duration      : {duration:.1f}s")
    print(f"  Time per line : {duration / len(lines):.2f}s")

    print(f"Writing {DEFAULT_OUTPUT_ASS}...")
    write_scroll_ass(lines, DEFAULT_OUTPUT_ASS, duration)

    print(f"Generating {DEFAULT_OUTPUT_MP4}...")
    make_video(DEFAULT_INPUT_WAV, DEFAULT_OUTPUT_ASS, DEFAULT_OUTPUT_MP4)


if __name__ == "__main__":
    main()
