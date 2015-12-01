#! /bin/bash

if [ ! -f cuda_7.5.18_linux.run ]; then
        wget http://aolab-utilities.s3.amazonaws.com/cuda_7.5.18_linux.run
fi

if [ ! -f cudnn-7.0-linux-x64-v3.0-prod.tgz ]; then
        wget http://aolab-utilities.s3.amazonaws.com/cudnn-7.0-linux-x64-v3.0-prod.tgz
fi

if [ ! -f NVIDIA-Linux-x86_64-352.63.run ]; then
        wget http://aolab-utilities.s3.amazonaws.com/NVIDIA-Linux-x86_64-352.63.run
fi

if [ ! -f Anaconda2-2.4.0-Linux-x86_64.sh ]; then
	wget http://aolab-utilities.s3.amazonaws.com/Anaconda2-2.4.0-Linux-x86_64.sh
fi

if [ ! -f fast_rcnn_models.tgz ]; then
	wget http://aolab-utilities.s3.amazonaws.com/fast_rcnn_models.tgz
fi

if [ ! -f 3.0.0.zip ]; then
	wget http://aolab-utilities.s3.amazonaws.com/3.0.0.zip
fi

if [ ! -f caffe.tar.gz ]; then
	wget http://aolab-utilities.s3.amazonaws.com/caffe.tar.gz
fi

if [ ! -f cnn_age_gender_models_and_data.0.0.2.zip ]; then
	wget http://aolab-utilities.s3.amazonaws.com/cnn_age_gender_models_and_data.0.0.2.zip
fi

if [ ! -f fast-rcnn.tar.gz ]; then
	wget http://aolab-utilities.s3.amazonaws.com/fast-rcnn.tar.gz
fi

if [ ! -f dlib.tar.gz ]; then
	wget http://aolab-utilities.s3.amazonaws.com/dlib.tar.gz
fi

docker build -t mitmul/cvmodules:1.0 .
