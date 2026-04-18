import re
import os
import sys
import configparser

GAP_THRESHOLD = 1.0  # seconds — blank line inserted between entries with gap larger than this


def load_config(config_path="../5_content_creator/config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]


def srt_time_to_sec(t):
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def parse_srt(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    entries = []
    for block in re.split(r"\n\n+", content.strip()):
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        m = re.match(r"(\S+) --> (\S+)", lines[1])
        if not m:
            continue
        entries.append({
            "timestamp": lines[1],
            "start":     srt_time_to_sec(m.group(1)),
            "end":       srt_time_to_sec(m.group(2)),
            "text":      " ".join(lines[2:]),
        })
    return entries


def convert(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    entries = parse_srt(input_path)
    if not entries:
        print("No subtitle entries found.")
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for i, e in enumerate(entries):
            f.write(e["text"] + "\n")
            if i < len(entries) - 1:
                gap = entries[i + 1]["start"] - e["end"]
                if gap > GAP_THRESHOLD:
                    f.write("\n")

    print(f"Saved {len(entries)} lines → {output_path}")


if __name__ == "__main__":
    _cfg = load_config()
    DEFAULT_INPUT  = _cfg["filelocation.elevenlab2sub"] + _cfg["prefix.elevenlab2sub"] + "." + _cfg["extention.elevenlab2sub"]
    DEFAULT_OUTPUT = _cfg["filelocation.lyrics"]        + _cfg["prefix.lyrics"]        + "." + _cfg["extention.lyrics"]
    convert(DEFAULT_INPUT, DEFAULT_OUTPUT)
