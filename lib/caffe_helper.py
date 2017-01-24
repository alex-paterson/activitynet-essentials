import numpy as np
import caffe
from image_helper import ImageHelper

class CaffeHelper:

    def __init__(self, net_path, model_path, mean_path):
        caffe.set_device(0)
        caffe.set_mode_gpu()
        self.net = caffe.Net(net_path, model_path, caffe.TRAIN)

        # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2,0,1))
        self.transformer.set_mean('data', np.load(mean_path).mean(1).mean(1)) # mean pixel
        self.transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
        self.transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

        self.net.blobs['data'].reshape(1,3,227,227)

    def get_layer_representation(self, frame, layer_name='fc8'):
        self.net.blobs['data'].data[...] = self.transformer.preprocess('data', frame)
        out = self.net.forward()
        repre = self.net.blobs[layer_name].data
        return repre
