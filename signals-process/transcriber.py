import subprocess
import os

# --- CONFIGURATION ---
# Just point to your MP3 file. No manual conversion needed!
filename = "mymusic.mp3" 
# ---------------------

def separate_vocals_direct(audio_file):
    current_dir = os.getcwd()
    input_path = os.path.join(current_dir, audio_file)
    output_path = os.path.join(current_dir, "separated_results")

    if not os.path.exists(input_path):
        print(f"Error: {audio_file} not found in {current_dir}")
        return

    # The command stays exactly the same
    command = [
        "demucs",
        "-n", "htdemucs",
        "--two-stems", "vocals",
        "-o", output_path,
        input_path
    ]

    print(f"Reading MP3 and extracting vocals...")
    subprocess.run(command, check=True)
    
    song_name = os.path.splitext(audio_file)[0]
    print(f"Finished! Your isolated voice is at: {output_path}/htdemucs/{song_name}/vocals.wav")

if __name__ == "__main__":
    separate_vocals_direct(filename)