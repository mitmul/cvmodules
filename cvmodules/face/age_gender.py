#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'caffe/build/install/python')
import caffe


class AgeGender(object):

    def __init__(self):
        data_dir = 'cnn_age_gender_models_and_data.0.0.2'
        mean_filename = '{}/mean.binaryproto'.format(data_dir)
        proto_data = open(mean_filename, "rb").read()
        a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
        mean = caffe.io.blobproto_to_array(a)[0]
        mean = mean.mean(1).mean(1)

        age_net_pretrained = '{}/age_net.caffemodel'.format(data_dir)
        age_net_model_file = '{}/deploy_age.prototxt'.format(data_dir)
        self.age_net = caffe.Classifier(age_net_model_file, age_net_pretrained,
                                        mean=mean,
                                        channel_swap=(2, 1, 0),
                                        raw_scale=255,
                                        image_dims=(256, 256))

        gender_net_pretrained = '{}/gender_net.caffemodel'.format(data_dir)
        gender_net_model_file = '{}/deploy_gender.prototxt'.format(data_dir)
        self.gender_net = caffe.Classifier(gender_net_model_file, gender_net_pretrained,
                                           mean=mean,
                                           channel_swap=(2, 1, 0),
                                           raw_scale=255,
                                           image_dims=(256, 256))

        self.age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
                         '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
        self.gender_list = ['Male', 'Female']

    def get_age_gender(self, img):
        age = self.age_net.predict([img])
        gen = self.gender_net.predict([img])
        age = self.age_list[age[0].argmax()]
        gen = self.gender_list[gen[0].argmax()]

        return age, gen


if __name__ == '__main__':
    age_gender = AgeGender()
    img = caffe.io.load_image('young.png')
    print age_gender.get_age_gender(img)
