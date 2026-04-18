import subprocess
import os
import sys
import configparser
import torch
import torchaudio

# Silences non-speech regions in a WAV file using SileroVAD.
# Unlike cutting, duration is fully preserved — only flute-only sections go silent.
# Regions where voice and flute overlap are untouched (VAD detects them as speech).

VAD_THRESHOLD   = 0.5
MIN_SPEECH_MS   = 100
MIN_SILENCE_MS  = 400
SPEECH_PAD_MS   = 300
VAD_SAMPLE_RATE = 16000


def load_config(config_path="../5_content_creator/config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]


def load_vad_model():
    model, utils = torch.hub.load(
        repo_or_dir="snakers4/silero-vad",
        model="silero_vad",
        force_reload=False,
    )
    get_speech_timestamps, _, read_audio, _, _ = utils
    return model, get_speech_timestamps, read_audio


def get_speech_segments(wav_path, model, get_speech_timestamps, read_audio):
    """Returns speech timestamps in seconds using a 16kHz resampled copy."""
    wav = read_audio(wav_path, sampling_rate=VAD_SAMPLE_RATE)
    timestamps = get_speech_timestamps(
        wav, model,
        sampling_rate=VAD_SAMPLE_RATE,
        threshold=VAD_THRESHOLD,
        min_speech_duration_ms=MIN_SPEECH_MS,
        min_silence_duration_ms=MIN_SILENCE_MS,
        speech_pad_ms=SPEECH_PAD_MS,
    )
    return [(t["start"] / VAD_SAMPLE_RATE, t["end"] / VAD_SAMPLE_RATE) for t in timestamps]


def silence_non_speech(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    print(f"Loading: {input_path}")
    waveform, sample_rate = torchaudio.load(input_path)

    print("Loading SileroVAD model...")
    model, get_speech_timestamps, read_audio = load_vad_model()

    print("Detecting speech segments...")

    # Resample to 16kHz mono for VAD if needed
    if sample_rate != VAD_SAMPLE_RATE:
        vad_waveform = torchaudio.functional.resample(waveform, sample_rate, VAD_SAMPLE_RATE)
        vad_mono = vad_waveform.mean(dim=0)
    else:
        vad_mono = waveform.mean(dim=0)

    timestamps = get_speech_timestamps(
        vad_mono, model,
        sampling_rate=VAD_SAMPLE_RATE,
        threshold=VAD_THRESHOLD,
        min_speech_duration_ms=MIN_SPEECH_MS,
        min_silence_duration_ms=MIN_SILENCE_MS,
        speech_pad_ms=SPEECH_PAD_MS,
    )

    print(f"  Detected {len(timestamps)} speech segments")

    if not timestamps:
        print("Warning: no speech detected — output will be silent.")

    # Build a silence mask at the original sample rate, then fill in speech regions
    total_samples = waveform.shape[1]
    mask = torch.zeros(total_samples)

    for t in timestamps:
        start = int(t["start"] / VAD_SAMPLE_RATE * sample_rate)
        end   = min(int(t["end"]   / VAD_SAMPLE_RATE * sample_rate), total_samples)
        mask[start:end] = 1.0

    filtered = waveform * mask.unsqueeze(0)

    speech_sec = mask.sum().item() / sample_rate
    total_sec  = total_samples / sample_rate
    silenced_sec = total_sec - speech_sec
    print(f"  Total duration : {total_sec:.1f}s")
    print(f"  Speech kept    : {speech_sec:.1f}s")
    print(f"  Silenced       : {silenced_sec:.1f}s (flute-only regions)")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    torchaudio.save(output_path, filtered, sample_rate)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    _cfg = load_config()
    DEFAULT_INPUT  = _cfg["filelocation.vocals"]     + _cfg["prefix.vocals"]     + "." + _cfg["extention.vocals"]
    DEFAULT_OUTPUT = _cfg["filelocation.before_sub"] + _cfg["prefix.before_sub"] + "." + _cfg["extention.before_sub"]
    silence_non_speech(DEFAULT_INPUT, DEFAULT_OUTPUT)