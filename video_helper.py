import os
import subprocess as sp
from . import ROOT_DIR

FFMPEG_BIN = 'ffmpeg'
YOUTUBEDL_BIN = 'youtube-dl'
VIDEOS_PATH = os.path.join(ROOT_DIR, "videos/")

class VideoHelper:
    @staticmethod
    def download_video_by_id(video_id):
        command = [ YOUTUBEDL_BIN,
                    '-f', 'best',
                    '-f', 'mp4',
                    "https://www.youtube.com/watch?v={}".format(video_id),
                    '-o', os.path.join(VIDEOS_PATH, "v_{}.mp4".format(video_id))]
        pipe = sp.call(command)

    @staticmethod
    def download_video_by_url(video_url):
        command = [ YOUTUBEDL_BIN,
                    '-f', 'best',
                    '-f', 'mp4',
                    video_url,
                    '-o', os.path.join(VIDEOS_PATH, "v_{}.mp4".format(video_url[-11:-1]))]
        s = ""
        for i in command:
            s = s + " " + i
        print(s)
        pipe = sp.call(command)

    @staticmethod
    def delete_all_videos():
        for file in os.listdir(VIDEOS_PATH):
            file_path = os.path.join(VIDEOS_PATH, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print("VideoHelper[delete_all_videos] {}".format(e))
