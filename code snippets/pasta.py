from ActivityNet import ActivityNet, VideoHelper, ImageHelper
import numpy as np
from PIL import Image

act_net = ActivityNet(2)

pasta_objects = act_net.get_subset_with_label('training', 'Preparing pasta')
pasta_object = pasta_objects[0]

# for pobject in pasta_objects:
#     print pobject

pasta_url = pasta_object['url']
pasta_annotations = pasta_object['annotations']
pasta_annotation = pasta_annotations[0]

# VideoHelper.download_video_by_url(pasta_url)
pasta_video_reader = VideoHelper.open_video_by_url(pasta_url)
pasta_frames, shape = VideoHelper.get_frames_per_second_with_dimensions(pasta_video_reader, 2, pasta_annotation, 360, 480)

print(shape)
# print(pasta_frames.shape)
#

ImageHelper.show_image(pasta_frames[6])

# image = pasta_frames[0]
# image_pil = Image.fromarray(image)
# image_pil = image_pil.resize((480, 360), Image.ANTIALIAS)
# image = np.asarray(image_pil)

# VideoHelper.reshape_video(pasta_frames, (480,360))
