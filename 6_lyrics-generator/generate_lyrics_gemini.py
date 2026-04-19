import sys
import os
import configparser
from google import genai
from google.genai import types


def load_config(config_path="../5_content_creator/config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]


_cfg = load_config()

OUTPUT_LYRICS = (
    _cfg["filelocation.lyrics"]
    + _cfg["prefix.lyrics"]
    + "."
    + _cfg["extention.lyrics"]
)

DEFAULT_PROMPT = _cfg.get("api.gemini.prompt", "").strip()

API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Free tier model available on this account
MODEL = "models/gemini-2.0-flash-lite"

SYSTEM_INSTRUCTION = """\
You are a Bengali lyrics expert. When given a song title or hints, return the full \
original Bengali lyrics in Bengali script (বাংলা).

Rules:
- Output ONLY the lyrics — no intro, no labels, no explanations, no English
- Separate verses with a blank line
- If the song has a chorus, include it where it naturally repeats
- Preserve the original words exactly as written/sung
"""


def fetch_lyrics(prompt: str) -> str:
    client = genai.Client(api_key=API_KEY)

    print(f"  Model : {MODEL}")
    print(f"  Prompt: {prompt}")

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
        ),
    )
    return response.text.strip()


def save_lyrics(lyrics: str, output_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(lyrics + "\n")
    print(f"  Saved: {output_path}")


def main():
    if not API_KEY:
        print("Error: GEMINI_API_KEY not set.")
        print("  Run: source ../git-ignore-files/os_env_variable.sh")
        sys.exit(1)

    prompt = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROMPT

    if not prompt:
        print("Error: no prompt provided.")
        print("  Set in config.properties:  api.gemini.prompt = lyrics for ...")
        sys.exit(1)

    print("Fetching lyrics via Gemini...")
    lyrics = fetch_lyrics(prompt)

    print("\n--- Lyrics ---")
    print(lyrics)
    print("--------------\n")

    save_lyrics(lyrics, OUTPUT_LYRICS)


if __name__ == "__main__":
    main()
