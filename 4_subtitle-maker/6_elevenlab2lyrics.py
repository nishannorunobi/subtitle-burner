import json
import os
import sys
import configparser

SENTENCE_ENDINGS = {"।", "।"}
GAP_THRESHOLD    = 1.0  # seconds — blank line inserted between sentences with gap larger than this


def load_config(config_path="../5_content_creator/config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]


def sec_to_srt_time(seconds):
    ms = int(round(seconds * 1000))
    h  = ms // 3_600_000;  ms %= 3_600_000
    m  = ms // 60_000;     ms %= 60_000
    s  = ms // 1_000;      ms %= 1_000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_sentences(words):
    sentences = []
    current_words = []
    start = None

    for w in words:
        if w["type"] != "word":
            continue
        if start is None:
            start = w["start"]
        current_words.append(w["text"])
        if any(w["text"].endswith(p) for p in SENTENCE_ENDINGS):
            sentences.append({
                "text":      " ".join(current_words),
                "start":     start,
                "end":       w["end"],
                "timestamp": f"{sec_to_srt_time(start)} --> {sec_to_srt_time(w['end'])}",
            })
            current_words = []
            start = None

    if current_words:
        last_end = next((w["end"] for w in reversed(words) if w["type"] == "word"), 0)
        sentences.append({
            "text":      " ".join(current_words),
            "start":     start,
            "end":       last_end,
            "timestamp": f"{sec_to_srt_time(start)} --> {sec_to_srt_time(last_end)}",
        })

    return sentences


def convert(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    sentences = build_sentences(data["words"])
    if not sentences:
        print("No sentences found.")
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sentences[0]["timestamp"] + "\n")

        for i, s in enumerate(sentences):
            f.write(s["text"] + "\n")
            if i < len(sentences) - 1:
                gap = sentences[i + 1]["start"] - s["end"]
                if gap > GAP_THRESHOLD:
                    f.write("\n")

        f.write(sentences[-1]["timestamp"] + "\n")

    print(f"Saved {len(sentences)} lines -> {output_path}")


if __name__ == "__main__":
    _cfg = load_config()
    DEFAULT_INPUT  = _cfg["filelocation.elevenlab"] + _cfg["prefix.elevenlab"] + "." + _cfg["extention.elevenlab.file"]
    DEFAULT_OUTPUT = _cfg["filelocation.lyrics"]    + _cfg["prefix.lyrics"]    + "." + _cfg["extention.lyrics"]
    convert(DEFAULT_INPUT, DEFAULT_OUTPUT)
