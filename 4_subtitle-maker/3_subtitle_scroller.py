import re
import subprocess
import os
import sys

# --- Constants ---
DEFAULT_INPUT_MP4  = "../git-ignore-files/2_2_2_no_pause.mp4"
DEFAULT_LYRICS_TXT = "../git-ignore-files/lyrics.txt"
DEFAULT_OUTPUT_ASS = "scroll.ass"
DEFAULT_OUTPUT_MP4 = "../git-ignore-files/4_3_4_scroll_sub.mp4"

# Video
VIDEO_CODEC   = "libx264"
AUDIO_CODEC   = "aac"
AUDIO_BITRATE = "192k"

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
LINE_HEIGHT = 80    # approx pixel height per line at FONT_SIZE 60


TIMESTAMP_RE = re.compile(
    r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})"
)


def srt_time_to_seconds(t):
    h, m, s_ms = t.split(":")
    s, ms = s_ms.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def parse_lyrics(lyrics_path):
    with open(lyrics_path, "r", encoding="utf-8-sig") as f:
        raw = f.read().replace("\r\n", "\n").replace("\r", "\n")

    start_time = None
    end_time   = None
    lines      = []

    for line in raw.splitlines():
        line = line.strip()
        m = TIMESTAMP_RE.match(line)
        if m:
            t = srt_time_to_seconds(m.group(1))
            if start_time is None:
                start_time = t
            else:
                end_time = t
            continue
        if line:
            lines.append(line)

    return lines, start_time, end_time


def fmt_ass_time(t):
    h  = int(t // 3600)
    m  = int((t % 3600) // 60)
    s  = int(t % 60)
    cs = int((t - int(t)) * 100)
    return f"{h}:{m:02}:{s:02}.{cs:02}"


def write_scroll_ass(lines, ass_path, start_time, end_time):
    n         = len(lines)
    available = end_time - start_time

    # Speed chosen so all lines scroll continuously across available time
    # Total scroll distance = screen height + all lines stacked
    speed         = (PLAY_RES_Y + n * LINE_HEIGHT) / available
    traverse_time = (PLAY_RES_Y + LINE_HEIGHT) / speed
    spacing       = LINE_HEIGHT / speed

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

    cx      = PLAY_RES_X // 2
    start_y = PLAY_RES_Y + LINE_HEIGHT // 2   # enters from below screen
    end_y   = -(LINE_HEIGHT // 2)             # exits above screen

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header)
        for i, line in enumerate(lines):
            t_start  = start_time + (i - 2) * spacing
            t_end    = t_start + traverse_time
            move_tag = f"{{\\move({cx},{start_y},{cx},{end_y})}}"
            f.write(
                f"Dialogue: 0,{fmt_ass_time(t_start)},"
                f"{fmt_ass_time(t_end)},Default,,0,0,0,,{move_tag}{line}\n"
            )


def make_video(input_mp4, ass_path, output_path):
    abs_ass = os.path.abspath(ass_path).replace("\\", "/").replace(":", "\\:")
    cmd = [
        "ffmpeg", "-y",
        "-i", os.path.abspath(input_mp4),
        "-vf", f"ass={abs_ass}",
        "-c:v", VIDEO_CODEC,
        "-c:a", AUDIO_CODEC,
        "-b:a", AUDIO_BITRATE,
        os.path.abspath(output_path),
    ]
    subprocess.run(cmd, check=True)
    print(f"Saved: {output_path}")


def main():
    print(f"Parsing {DEFAULT_LYRICS_TXT}...")
    lines, start_time, end_time = parse_lyrics(DEFAULT_LYRICS_TXT)
    print(f"  {len(lines)} lyric lines loaded")
    print(f"  Time range: {start_time:.1f}s → {end_time:.1f}s")

    if start_time is None or end_time is None:
        print("Error: could not find start/end timestamps in lyrics file")
        sys.exit(1)

    print(f"Writing {DEFAULT_OUTPUT_ASS}...")
    write_scroll_ass(lines, DEFAULT_OUTPUT_ASS, start_time, end_time)

    print(f"Generating {DEFAULT_OUTPUT_MP4}...")
    make_video(DEFAULT_INPUT_MP4, DEFAULT_OUTPUT_ASS, DEFAULT_OUTPUT_MP4)


if __name__ == "__main__":
    main()
