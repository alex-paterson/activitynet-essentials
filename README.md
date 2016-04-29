# ActivityNet Essentials

A couple of python classes to help deal with the ActivityNet dataset. Video related methods require youtube-dl and ffmpeg installed as commandline apps
(they're called by subprocess).

## ActivityNet

```
from ActivityNet import ActivityNet

act_net = ActivityNet(2) #or ActivityNet(3) depending on version
act_net.print_taxonomy_tree()
tax_tree = act_net.get_taxonomy_tree()

train_data = act_net.get_subset('train')
pasta_training_data = act_net.get_subset_with_label('training', 'Preparing pasta')
```

## VideoHelper

```
from ActivityNet import ActivityNet, VideoHelper

act_net = ActivityNet(2)
pasta_url = act_net.get_subset_with_label('training', 'Preparing pasta')[0]['url']
VideoHelper.download_video_by_url(pasta_url)
VideoHelper.delete_all_videos()
```
