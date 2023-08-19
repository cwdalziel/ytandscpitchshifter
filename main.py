from pytube import YouTube
from pydub import AudioSegment
from pathlib import Path
from sclib import SoundcloudAPI, Track
import tempfile
import os

while True:
    url = input('Enter a YouTube or SoundCloud track URL:')
    try:
        yt = YouTube(url)
        with tempfile.TemporaryDirectory() as temp:
            file = yt.streams.get_audio_only().download(temp)
            audio = AudioSegment.from_file(file)
        filename = file.__str__().split("\\")[-1][:-4]
        break
    except:
        try:
            track = SoundcloudAPI().resolve(url)
            assert type(track) is Track
            filename = f'./{track.artist} - {track.title}.mp3'
            cwd = os.getcwd()
            with tempfile.TemporaryDirectory() as temp:
                os.chdir(temp)
                with open(filename, 'wb+') as file:
                    track.write_mp3_to(file)
                    audio = AudioSegment.from_file(file)
                os.chdir(cwd)
            filename = filename[:-4]
            break
        except:
            print("Invalid URL, try again")

while True:
    try:
        semitones = int(input("How many semitones should the audio be shifted?: "))
        break
    except:
        print("Invalid number of semitones, try again")

audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * (2 ** (1. / 12)) ** semitones)})
downloads = str(Path.home() / "Downloads")
final = audio.export(downloads + "\\" + filename + "(" + semitones.__str__() + " shift).mp3", format="mp3")

print("Saved as \"" + final.name + "\"")