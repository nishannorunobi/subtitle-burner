from pydub import AudioSegment

audio = AudioSegment.from_wav("input.wav")
audio.export("output.mp3", format="mp3")
