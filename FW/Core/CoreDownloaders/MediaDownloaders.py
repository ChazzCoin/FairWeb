from __future__ import unicode_literals
import os
import subprocess
import youtube_dl
from pytube import YouTube
from F import OS, FFMPEG

completedFolder = f"{OS.get_cwd()}/completed"

ydl_options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

def post_processor():
    for file in OS.get_files_in_directory(completedFolder):
        if str(file).endswith(".mp4"):
            newFile = str(file)[:-4]
            newFile = f"{newFile}-rs"
            file = f"{completedFolder}/{file}"
            post_process(file, newFile)


def post_process(fileIn, fileOutName):
    fileNameOut = f"{OS.get_cwd()}/completed/{fileOutName}.mp3"
    output = subprocess.run(f"ffmpeg -i {fileIn} -b:a 192k {fileNameOut}", shell=True)
    return output

def YoutubeDownloader(url, toMp3=True):
    try:
        ytObj = YouTube(url)
        video = ytObj.streams.filter(only_audio=True).first()
        destination = 'completed'
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        mp4File = base + '.mp4'
        if toMp3:
            FFMPEG.to_mp3(mp4File)
            newMp4File = str(mp4File).replace(" ", "-")
            OS.rename_file(mp4File, newMp4File)
            os.remove(mp4File)
            return mp4File, url
        return mp4File, url
    except:
        return None

def GeneralDownloader(url):
    if type(url) not in [list]:
        url = [url]
    try:
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            ydl.download(url)
        return True, url
    except:
        return False, url

# from F import OS
# test = OS.get_cwd() + "/test.mp3"
# # post_process_two(test)
# post_processor()
# # YoutubeDownloader("https://www.youtube.com/watch?v=cHHLHGNpCSA")