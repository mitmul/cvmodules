#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'fast-rcnn/caffe-fast-rcnn/build/install/python')
sys.path.insert(1, 'fast-rcnn/lib')
sys.path.insert(2, 'dlib/python_examples')

import caffe
from fast_rcnn.test import im_detect
from utils.cython_nms import nms
import numpy as np
import dlib
import cv2 as cv
from skimage import io


class FastRCNNPrediction(object):

    def __init__(self):
        self.CLASSES = ('__background__',
                        'aeroplane', 'bicycle', 'bird', 'boat',
                        'bottle', 'bus', 'car', 'cat', 'chair',
                        'cow', 'diningtable', 'dog', 'horse',
                        'motorbike', 'person', 'pottedplant',
                        'sheep', 'sofa', 'train', 'tvmonitor')
        caffe.set_mode_gpu()
        caffe.set_device(0)

        # get network instance
        proto_fn = 'fast-rcnn/models/VGG16/test.prototxt'
        model_fn = 'fast-rcnn/data/fast_rcnn_models/'
        model_fn += 'vgg16_fast_rcnn_iter_40000.caffemodel'
        self.net = caffe.Net(proto_fn, model_fn, caffe.TEST)

    def bbox(self, img):
        rects = []
        dlib.find_candidate_object_locations(img, rects, min_size=500)
        bbox = np.array([[r.left(), r.top(), r.right(), r.bottom()]
                         for r in rects])

        return bbox

    def detect(self, img):
        bbox = self.bbox(img)

        scores, boxes = im_detect(self.net, img, bbox)

        result = []

        CONF_THRESH = 0.8
        NMS_THRESH = 0.3
        for cls in self.CLASSES[1:]:
            cls_ind = self.CLASSES.index(cls)
            cls_boxes = boxes[:, 4 * cls_ind:4 * (cls_ind + 1)]
            cls_scores = scores[:, cls_ind]
            dets = np.hstack((cls_boxes,
                              cls_scores[:, np.newaxis])).astype(np.float32)
            keep = nms(dets, NMS_THRESH)
            dets = dets[keep, :]

            inds = np.where(dets[:, -1] >= CONF_THRESH)[0]
            if len(inds) == 0:
                continue

            for i in inds:
                bbox = dets[i, :4]
                x1, y1, x2, y2 = map(int, bbox)
                result.append({
                    "label": cls,
                    "bbox": [x1, y1, x2, y2]
                })

        return result


if __name__ == '__main__':
    img_fn = '2007_000129.jpg'
    img = io.imread(img_fn)

    fast_rcnn = FastRCNNPrediction()
    result, img = fast_rcnn.detect(img)
    io.imsave('2007_000129_det.jpg', img)

    print result
