import sys
import os
import base64
import configparser
import anthropic


def load_config(config_path="../5_content_creator/config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]


_cfg = load_config()

DEFAULT_INPUT_WAV = (
    _cfg["filelocation.before_sub"]
    + _cfg["prefix.before_sub"]
    + "."
    + _cfg["extention.before_sub"]
)

OUTPUT_LYRICS = (
    _cfg["filelocation.lyrics"]
    + _cfg["prefix.lyrics"]
    + "."
    + _cfg["extention.lyrics"]
)

SYSTEM_PROMPT = """\
You are an expert Bengali lyricist. Listen carefully to the music provided and write \
authentic, emotionally resonant Bengali song lyrics that match its mood, tempo, and feel.

Guidelines:
- Write in pure Bengali script (বাংলা)
- Match the emotional tone of the music (sad, joyful, devotional, romantic, energetic, etc.)
- Each line should be singable — natural rhythm that fits the music's pace
- Keep lines concise (5–10 words each)
- Separate verses with a blank line
- No Roman transliteration, no English words
- Output ONLY the lyrics — no titles, labels, or explanations
"""


def generate_lyrics(wav_path: str, num_lines: int = 24) -> str:
    print(f"  Reading: {wav_path}")
    with open(wav_path, "rb") as f:
        audio_data = base64.standard_b64encode(f.read()).decode("utf-8")

    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2048,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "audio",
                        "source": {
                            "type": "base64",
                            "media_type": "audio/wav",
                            "data": audio_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            f"Listen to this music and write Bengali lyrics that match "
                            f"its mood and rhythm. "
                            f"Approximately {num_lines} lines total, in 3–4 verses."
                        ),
                    },
                ],
            }
        ],
    )

    usage = response.usage
    print(f"  Tokens — input: {usage.input_tokens}, output: {usage.output_tokens}", end="")
    if usage.cache_creation_input_tokens:
        print(f", cache written: {usage.cache_creation_input_tokens}", end="")
    if usage.cache_read_input_tokens:
        print(f", cache hit: {usage.cache_read_input_tokens}", end="")
    print()

    return response.content[0].text.strip()


def save_lyrics(lyrics: str, output_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(lyrics + "\n")
    print(f"  Saved: {output_path}")


def main():
    wav_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT_WAV
    num_lines = int(sys.argv[2]) if len(sys.argv) > 2 else 24

    if not os.path.exists(wav_path):
        print(f"Error: file not found: {wav_path}")
        sys.exit(1)

    print(f"Generating Bengali lyrics from: {wav_path}")
    lyrics = generate_lyrics(wav_path, num_lines)

    print("\n--- Generated Lyrics ---")
    print(lyrics)
    print("------------------------\n")

    save_lyrics(lyrics, OUTPUT_LYRICS)


if __name__ == "__main__":
    main()
