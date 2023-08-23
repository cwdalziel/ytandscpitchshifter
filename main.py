from pytube import YouTube
from pydub import AudioSegment
from pathlib import Path
from sclib import SoundcloudAPI, Track
import tempfile
import os

# loops until valid link is used
while True:
    url = input('Enter a YouTube or SoundCloud track URL:')
    try:
        # downloads video as mp4 in temp directory then gets audio for AudioSegment and deletes
        yt = YouTube(url)
        with tempfile.TemporaryDirectory() as temp:
            file = yt.streams.get_audio_only().download(temp)
            audio = AudioSegment.from_file(file)
        filename = file.__str__().split("\\")[-1][:-4]
        break
    except:
        try:
            # gets soundcloud link, asserts it's a track, creates new temp directory and sets as working directory,
            # writes mp3 to be used in audio segment before closing temp directory and resetting working directory
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

# gets float input for audio pitch change
while True:
    try:
        semitones = float(input("How many semitones should the audio be shifted?: "))
        break
    except:
        print("Invalid number of semitones, try again")

# changes audio speed by changing audio frame rate
audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * (2 ** (1. / 12)) ** semitones)})

# finds download folder to use as directory parameter for file export
downloads = str(Path.home() / "Downloads")
final = audio.export(downloads + "\\" + filename + "(" + semitones.__str__() + " shift).mp3", format="mp3")
print("Saved as \"" + final.name + "\"")

# keeps .exe open
input("")
