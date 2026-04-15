import re
import subprocess
import argparse
import os
import sys

# --- Constants ---
DEFAULT_AUDIO      = "../3_media-converters/no-pause.mp4"
DEFAULT_SRT        = "bangla_subtitles.srt"
DEFAULT_OUTPUT_ASS = "output.ass"
DEFAULT_OUTPUT_MP4 = "subtitle-embedded.mp4"

# Video
VIDEO_RESOLUTION   = "1280x720"
VIDEO_FPS          = "25"
BG_COLOR           = "black"
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
    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    segments = []
    blocks = re.split(r"\n\n+", content.strip())

    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 2:
            continue
        time_match = re.match(
            r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})",
            lines[1],
        )
        if not time_match:
            continue
        start = srt_time_to_seconds(time_match.group(1))
        end   = srt_time_to_seconds(time_match.group(2))
        text  = " ".join(lines[2:]).strip()
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
    play_res_x, play_res_y = VIDEO_RESOLUTION.split("x")
    header = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        f"PlayResX: {play_res_x}\n"
        f"PlayResY: {play_res_y}\n"
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


def make_video(audio_path, ass_path, output_path):
    ass_escaped = ass_path.replace("\\", "/").replace(":", "\\:")
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c={BG_COLOR}:s={VIDEO_RESOLUTION}:r={VIDEO_FPS}",
        "-i", audio_path,
        "-map", "0:v",
        "-map", "1:a",
        "-shortest",
        "-vf", f"ass={ass_escaped}",
        "-c:v", VIDEO_CODEC,
        "-c:a", AUDIO_CODEC,
        "-b:a", AUDIO_BITRATE,
        output_path,
    ]
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
        help=f"Input audio file (default: {DEFAULT_AUDIO})",
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
