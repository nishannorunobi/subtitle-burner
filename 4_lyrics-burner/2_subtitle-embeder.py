import re
import subprocess
import argparse
import os
import sys

# --- Constants ---
DEFAULT_AUDIO      = "../git-ignore-files/2_2_2_no_pause.mp4"
DEFAULT_SRT        = "../git-ignore-files/4_1_3_no_pause_ben.srt"
DEFAULT_OUTPUT_ASS = "output.ass"
DEFAULT_OUTPUT_MP4 = "../git-ignore-files/4_2_4_embedded_sub.mp4"

# Video
VIDEO_CODEC        = "libx264"
AUDIO_CODEC        = "aac"
AUDIO_BITRATE      = "192k"

# Subtitle style
FONT_NAME          = "Noto Sans Bengali"
FONT_SIZE          = "84"
FONT_COLOR         = "&H0000FFFF"   # yellow  (ASS format: &HAABBGGRR)
SECONDARY_COLOR    = "&H000000FF"
OUTLINE_COLOR      = "&H00000000"   # black
BACK_COLOR         = "&H80000000"   # semi-transparent
BOLD               = "-1"           # -1 = true
ITALIC             = "-1"           # -1 = true
OUTLINE_WIDTH      = "2"
ALIGNMENT          = "5"            # 5 = center screen


def srt_time_to_seconds(t):
    h, m, s_ms = t.split(":")
    s, ms = s_ms.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def parse_srt(srt_path):
    with open(srt_path, "r", encoding="utf-8-sig") as f:
        content = f.read()

    content = content.replace("\r\n", "\n").replace("\r", "\n")
    segments = []
    blocks = re.split(r"\n\n+", content.strip())

    TIME_RE = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})")
    for block in blocks:
        lines = block.strip().splitlines()
        if not lines:
            continue
        time_match = None
        time_idx = None
        for i, line in enumerate(lines):
            time_match = TIME_RE.match(line.strip())
            if time_match:
                time_idx = i
                break
        if not time_match:
            continue
        start = srt_time_to_seconds(time_match.group(1))
        end   = srt_time_to_seconds(time_match.group(2))
        text  = " ".join(lines[time_idx + 1:]).strip()
        if text:
            segments.append({"start": start, "end": end, "text": text})

    return segments


def fmt_ass_time(t):
    h  = int(t // 3600)
    m  = int((t % 3600) // 60)
    s  = int(t % 60)
    cs = int((t - int(t)) * 100)
    return f"{h}:{m:02}:{s:02}.{cs:02}"


def write_ass(segments, ass_path):
    header = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        "PlayResX: 1280\n"
        "PlayResY: 720\n"
        "ScaledBorderAndShadow: yes\n"
        "\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Default,{FONT_NAME},{FONT_SIZE},"
        f"{FONT_COLOR},{SECONDARY_COLOR},{OUTLINE_COLOR},{BACK_COLOR},"
        f"{BOLD},{ITALIC},0,0,100,100,0,0,1,{OUTLINE_WIDTH},0,{ALIGNMENT},10,10,30,1\n"
        "\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header)
        for seg in segments:
            text = seg["text"].replace("\n", "\\N")
            f.write(
                f"Dialogue: 0,{fmt_ass_time(seg['start'])},"
                f"{fmt_ass_time(seg['end'])},Default,,0,0,0,,{text}\n"
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
    print(f"ASS path : {abs_ass}")
    print(f"ASS exists: {os.path.exists(ass_path)}")
    print(f"FFmpeg cmd: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Bangla audio + SRT → MP4 video with burned subtitles"
    )
    parser.add_argument(
        "audio",
        nargs="?",
        default=DEFAULT_AUDIO,
        help=f"Input MP4 file (default: {DEFAULT_AUDIO})",
    )
    parser.add_argument(
        "--srt",
        default=DEFAULT_SRT,
        help=f"SRT subtitle file (default: {DEFAULT_SRT})",
    )
    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"Error: audio file not found: {args.audio}")
        sys.exit(1)

    if not os.path.exists(args.srt):
        print(f"Error: SRT file not found: {args.srt}")
        sys.exit(1)

    print(f"Parsing {args.srt}...")
    segments = parse_srt(args.srt)
    print(f"  {len(segments)} subtitle entries loaded")

    print(f"Writing {DEFAULT_OUTPUT_ASS}...")
    write_ass(segments, DEFAULT_OUTPUT_ASS)

    print(f"Generating {DEFAULT_OUTPUT_MP4}...")
    make_video(args.audio, DEFAULT_OUTPUT_ASS, DEFAULT_OUTPUT_MP4)


if __name__ == "__main__":
    main()
