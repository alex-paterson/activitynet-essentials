import os, imageio
import subprocess as sp
import numpy as np

from .image_helper import ImageHelper

FFMPEG_BIN = 'ffmpeg'
YOUTUBEDL_BIN = 'youtube-dl'

class VideoHelper:
    def __init__(self, videos_path):
        if not os.path.exists(videos_path):
            os.makedirs(videos_path)
        self.videos_path = videos_path

    def download_video_by_id(self, video_id):
        command = [ YOUTUBEDL_BIN,
                    '-f', 'best',
                    '-f', 'mp4',
                    "https://www.youtube.com/watch?v={}".format(video_id),
                    '-o', os.path.join(self.videos_path, "v_{}.mp4".format(video_id))]
        pipe = sp.call(command)

    def download_video_by_url(self, video_url):
        if not self.check_for_video_by_url(video_url):
            command = [ YOUTUBEDL_BIN,
                        '-f', 'best',
                        '-f', 'mp4',
                        video_url,
                        '-o', os.path.join(self.videos_path, "v_{}.mp4".format(video_url[-11:-1]))]
            s = ""
            for i in command:
                s = s + " " + i
            pipe = sp.call(command)
        else:
            print("[youtube] File already exists", video_url)


    def delete_all_videos(self):
        for file in os.listdir(self.videos_path):
            file_path = os.path.join(self.videos_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print("VideoHelper[delete_all_videos] {}".format(e))

    def open_video_by_id(self, id):
        filename = os.path.join(self.videos_path, "v_{}.mp4".format(id))
        return imageio.get_reader(filename, 'ffmpeg')

    def open_video_by_url(self, url):
        return self.open_video_by_id(url[-11:-1])

    def check_for_video_by_url(self, url):
        try:
            self.open_video_by_id(url[-11:-1])
            return True
        except:
            return False

    def get_meta_by_id(self, id):
        return self.open_video_by_id(id).get_meta_data()

    def get_meta_by_url(self, url):
        return self.get_meta_by_id(url[-11:-1])

    @staticmethod
    def get_frames_per_second(reader, custom_fps, annotation):
        fps = reader.get_meta_data()['fps']
        width = reader.get_meta_data()['size'][0]
        height = reader.get_meta_data()['size'][1]
        range_seconds = annotation['segment']
        range_frames = [ int(x*fps) for x in range_seconds ]

        index_list = range(range_frames[0],range_frames[1],int(fps/custom_fps))
        number_of_frames = len(index_list)

        frames = np.zeros(( number_of_frames, height, width, 3 ), dtype='uint8')
        index = 0
        for frame_index in index_list:
            frames[index] = reader.get_data(frame_index)
            # print("Return frame {} is original frame {}".format(index, frame_index))
            index += 1

        return frames, frames.shape

    @staticmethod
    def get_frames_per_second_with_dimensions(reader, custom_fps, annotation, height, width):
        fps = reader.get_meta_data()['fps']
        # width = reader.get_meta_data()['size'][0]
        # height = reader.get_meta_data()['size'][1]
        range_seconds = annotation['segment']
        range_frames = [ int(x*fps) for x in range_seconds ]

        index_list = range(range_frames[0],range_frames[1],int(fps/custom_fps))
        number_of_frames = len(index_list)

        frames = np.zeros(( number_of_frames, height, width, 3 ), dtype='uint8')
        index = 0
        for frame_index in index_list:
            frames[index] = ImageHelper.resize_image(reader.get_data(frame_index), height, width)
            # print("Return frame {} is original frame {}".format(index, frame_index))
            index += 1

        return frames, frames.shape

    @staticmethod
    def reshape_video(frames, new_dimensions):
        height = new_dimensions[0]
        width = new_dimensions[1]
        frame_count = len(frames)
        new_frames = np.zeros(( frame_count, height, width, 3 ), dtype='uint8')
        for frame_index in range(frame_count):
            frame_pre_resize = frames[frame_index]
            new_frames[frame_index] = ImageHelper.resize_image(frame_pre_resize, height, width)
        return(new_frames)
