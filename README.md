# ActivityNet Essentials

A few python classes to help deal with the ActivityNet dataset.

Video downloading methods require youtube-dl installed as a commandline app (it's called by subprocess, see video_helper.py#download_video_by_id).

Video reading methods require ffmpeg (e.g. `imageio.get_reader(filename, 'ffmpeg')` in video_helper.py).

## ActivityNet

```
from ActivityNet import ActivityNet

act_net = ActivityNet(2) #or ActivityNet(3) depending on version
act_net.print_taxonomy_tree()
tax_tree = act_net.get_taxonomy_tree()

train_data = act_net.get_subset('train')
pasta_training_data = act_net.get_subset_with_label('training', 'Preparing pasta')
first_pasta_video_object = pasta_training_data[0]
print(first_pasta_video_object)
pasta_url = first_pasta_video_object['url']
pasta_annotations = first_pasta_video_object['annotations']
```

## VideoHelper

```
from ActivityNet import ActivityNet, VideoHelper

act_net = ActivityNet(2)

pasta_object = act_net.get_subset_with_label('training', 'Preparing pasta')[0]

pasta_url = pasta_object['url']
pasta_annotations = pasta_object['annotations']
pasta_annotation = pasta_annotations[0]

VideoHelper.download_video_by_url(pasta_url)
pasta_video_reader = VideoHelper.open_video_by_url(pasta_url)
pasta_frames, shape = VideoHelper.get_frames_per_second(pasta_video_reader, 2, pasta_annotation)
pasta_frame = pasta_frames[0]

VideoHelper.delete_all_videos()

```

## HDFHelper

```
import numpy as np

frames = np.array(['1.0','2.0','3.0'])

hdf5_object = HDFHelper("test")

print("\nCreating group and saving data to it.")
hdf5_object.create_group("/test_dir_1/test_dir_2")
hdf5_object.save_data("/test_dir_1/test_dir_2", "test_item", frames)

hdf5_object.print_file_structure()

print("\nNow reading the data we saved.")
data = hdf5_object.get_data("/test_dir_1/test_dir_2", "test_item")
print(data)

print("\nNow deleting only item in the root directory.")
hdf5_object.delete_path("/test_dir_1")

# Will print nothing - file is empty
hdf5_object.print_file_structure()

hdf5_object.close()
```
