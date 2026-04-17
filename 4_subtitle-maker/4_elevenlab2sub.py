import json
import os
import sys
import configparser

SENTENCE_ENDINGS = {"।", "।"}


def load_config(config_path="../5_content_creator/config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]


def ms_to_srt_time(seconds):
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

        text = w["text"]
        if start is None:
            start = w["start"]

        current_words.append(text)

        if any(text.endswith(p) for p in SENTENCE_ENDINGS):
            sentences.append({
                "text": " ".join(current_words),
                "start": start,
                "end": w["end"],
            })
            current_words = []
            start = None

    if current_words:
        sentences.append({
            "text": " ".join(current_words),
            "start": start,
            "end": words[-1]["end"],
        })

    return sentences


def convert(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    sentences = build_sentences(data["words"])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for i, s in enumerate(sentences, 1):
            f.write(f"{i}\n")
            f.write(f"{ms_to_srt_time(s['start'])} --> {ms_to_srt_time(s['end'])}\n")
            f.write(f"{s['text']}\n\n")

    print(f"Saved {len(sentences)} subtitles → {output_path}")


if __name__ == "__main__":
    _cfg = load_config()
    DEFAULT_INPUT  = _cfg["filelocation.elevenlab"] + _cfg["prefix.elevenlab"] + "." + _cfg["extention.elevenlab.file"]
    DEFAULT_OUTPUT = _cfg["filelocation.elevenlab2sub"] + _cfg["prefix.elevenlab2sub"] + "." + _cfg["extention.elevenlab2sub.file"]
    convert(DEFAULT_INPUT, DEFAULT_OUTPUT)
