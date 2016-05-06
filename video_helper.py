import os, imageio
import subprocess as sp
import numpy as np
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

    @staticmethod
    def open_video_by_id(id):
        filename = os.path.join(VIDEOS_PATH, "v_{}.mp4".format(id))
        return imageio.get_reader(filename,  'ffmpeg')

    @staticmethod
    def open_video_by_url(url):
        return VideoHelper.open_video_by_id(url[-11:-1])

    @staticmethod
    def get_meta_by_id(id):
        return VideoHelper.open_video_by_id(id).get_meta_data()

    @staticmethod
    def get_meta_by_url(url):
        return VideoHelper.get_meta_by_id(url[-11:-1])

    @staticmethod
    def get_frames_every_half_second(reader, annotation):
        fps = reader.get_meta_data()['fps']
        width = reader.get_meta_data()['size'][0]
        height = reader.get_meta_data()['size'][1]
        range_seconds = annotation['segment']
        range_frames = [ int(x*fps) for x in range_seconds ]

        number_of_frames = len(range(range_frames[0],range_frames[1],int(fps/2)))

        frames = np.zeros(( number_of_frames, height, width, 3 ))
        for frame in range(number_of_frames):
            frames[frame] = reader.get_data(frame)

        return frames, frames.shape

    @staticmethod
    def get_frames(reader, annotation):
        fps = reader.get_meta_data()['fps']
        width = reader.get_meta_data()['size'][0]
        height = reader.get_meta_data()['size'][1]
        range_seconds = annotation['segment']
        range_frames = [ int(x*fps) for x in range_seconds ]

        number_of_frames = len(range(range_frames[0],range_frames[1],int(fps/2)))

        frames = np.zeros(( number_of_frames, height, width, 3 ))
        for frame in range(number_of_frames):
            frames[frame] = reader.get_data(frame)

        return frames, frames.shape
