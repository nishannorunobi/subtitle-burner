import subprocess
import tempfile
import os
import sys
import configparser


def load_main_config(config_path="../5_content_creator/config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]


def load_local_config(config_path="config.properties"):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_string("[DEFAULT]\n" + f.read())
    return config["DEFAULT"]


def vlc_time_to_sec(value):
    """Parse VLC-style M.SS into total seconds. e.g. 2.22 → 142.0s, 10.05 → 605.0s"""
    parts = str(value).strip().split(".")
    minutes = int(parts[0])
    seconds = int(parts[1]) if len(parts) > 1 else 0
    return float(minutes * 60 + seconds)


def load_cuts(local_cfg):
    """Read all cut.N.start / cut.N.end pairs. Skips pairs where start == end == 0."""
    cuts = []
    n = 1
    while True:
        start_key = f"cut.{n}.start"
        end_key   = f"cut.{n}.end"
        if start_key not in local_cfg:
            break
        start = vlc_time_to_sec(local_cfg[start_key])
        end   = vlc_time_to_sec(local_cfg[end_key])
        if start == 0.0 and end == 0.0:
            n += 1
            continue
        if start >= end:
            print(f"Warning: cut.{n} skipped — start ({start}s) >= end ({end}s)")
            n += 1
            continue
        cuts.append((start, end))
        n += 1
    return cuts


def get_duration(path):
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path,
    ], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def get_keep_segments(cuts, total):
    """Invert cut ranges into keep ranges."""
    cuts_sorted = sorted(cuts, key=lambda x: x[0])
    keeps = []
    prev = 0.0
    for cut_start, cut_end in cuts_sorted:
        if cut_start > prev:
            keeps.append((prev, cut_start))
        prev = max(prev, cut_end)
    if prev < total:
        keeps.append((prev, total))
    return keeps


def apply_cuts(input_path, output_path, cuts):
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    total = get_duration(input_path)
    print(f"Input    : {input_path}")
    print(f"Duration : {total:.2f}s")
    print(f"Cuts     : {len(cuts)}")
    for i, (s, e) in enumerate(sorted(cuts, key=lambda x: x[0]), 1):
        print(f"  Cut {i}  : {s:.2f}s → {e:.2f}s  ({e - s:.2f}s removed)")

    for s, e in cuts:
        if s < 0 or e > total or s >= e:
            print(f"Error: invalid cut range {s:.2f}s → {e:.2f}s for file of {total:.2f}s")
            sys.exit(1)

    keeps = get_keep_segments(cuts, total)
    print(f"Segments kept: {len(keeps)}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        seg_files   = []
        concat_list = os.path.join(tmp, "concat.txt")

        for i, (start, end) in enumerate(keeps):
            seg_file = os.path.join(tmp, f"seg_{i:04d}.wav")
            subprocess.run([
                "ffmpeg", "-y", "-i", input_path,
                "-ss", str(start), "-to", str(end),
                seg_file,
            ], check=True, capture_output=True)
            seg_files.append(seg_file)

        with open(concat_list, "w") as f:
            for s in seg_files:
                f.write(f"file '{s}'\n")

        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_list,
            output_path,
        ], check=True, capture_output=True)

    final = get_duration(output_path)
    removed = total - final
    print(f"Output   : {output_path}")
    print(f"Duration : {final:.2f}s  (removed {removed:.2f}s total)")


if __name__ == "__main__":
    _main  = load_main_config()
    _local = load_local_config()

    cuts = load_cuts(_local)
    if not cuts:
        print("No cuts configured. Check config.properties.")
        sys.exit(0)

    INPUT  = _main["filelocation.vocals"]     + _main["prefix.vocals"]     + "." + _main["extention.vocals"]
    OUTPUT = _main["filelocation.before_sub"] + _main["prefix.before_sub"] + "." + _main["extention.before_sub"]

    apply_cuts(INPUT, OUTPUT, cuts)