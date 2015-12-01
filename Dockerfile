FROM ubuntu:14.04

ENV DEBIAN_FRONTEND "noninteractive"

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git vim zsh htop bmon build-essential wget curl unzip cmake cmake-curses-gui
RUN apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libboost-all-dev libhdf5-serial-dev libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler libatlas-base-dev gfortran
RUN apt-get clean && apt-get autoclean && apt-get autoremove

WORKDIR /root
COPY Anaconda2-2.4.0-Linux-x86_64.sh /root/
RUN cd /root && bash Anaconda2-2.4.0-Linux-x86_64.sh -b
ENV PATH /root/anaconda2/bin:$PATH
RUN conda update conda -y
RUN pip install lmdb
RUN pip install protobuf
RUN pip install bottle
RUN pip install easydict

COPY 3.0.0.zip /root/
RUN unzip 3.0.0.zip && rm -rf 3.0.0.zip
RUN mkdir -p /root/opencv-3.0.0/build && cd /root/opencv-3.0.0/build && \
    cmake \
    -DBUILD_DOCS=OFF \
    -DBUILD_JASPER=OFF \
    -DBUILD_JPEG=OFF \
    -DBUILD_OPENEXR=OFF \
    -DBUILD_PACKAGE=ON \
    -DBUILD_PERF_TESTS=ON \
    -DBUILD_PNG=OFF \
    -DBUILD_SHARED_LIBS=ON \
    -DBUILD_TBB=OFF \
    -DBUILD_TESTS=ON \
    -DBUILD_TIFF=ON \
    -DBUILD_WITH_DEBUG_INFO=OFF \
    -DBUILD_ZLIB=OFF \
    -DENABLE_FAST_MATH=ON \
    -DBUILD_opencv_python2=ON \
    -DBUILD_opencv_python3=OFF \
    -DBUILD_EXAMPLES=OFF \
    -DPYTHON2_EXECUTABLE=$HOME/anaconda2/bin/python \
    -DPYTHON2_INCLUDE_DIR=$HOME/anaconda2/include/python2.7 \
    -DPYTHON_INCLUDE_DIR2=$HOME/anaconda2/include/python2.7 \
    -DPYTHON2_LIBRARY=$HOME/anaconda2/lib/libpython2.7.so \
    -DPYTHON2_PACKAGES_PATH=$HOME/anaconda2/lib/python2.7/site-packages \
    -DPYTHON_INCLUDE_DIR=$HOME/anaconda2/include/python2.7 \
    -DPYTHON_LIBRARY=$HOME/anaconda2/lib/libpython2.7.so \
    -DENABLE_AVX=ON \
    -DENABLE_SSE=ON \
    -DENABLE_SSE2=ON \
    -DENABLE_SSE3=ON \
    -DENABLE_SSE41=ON \
    -DENABLE_SSE42=ON \
    -DENABLE_SSSE3=ON \
    -DWITH_OPENCL=OFF \
    -DWITH_OPENCLAMDBLAS=OFF \
    -DWITH_OPENCLAMDFFT=OFF \
    -DWITH_OPENCL_SVM=OFF \
    -DWITH_OPENEXR=OFF \
    -DWITH_CUBLAS=OFF \
    -DWITH_CUDA=OFF \
    -DWITH_CUFFT=OFF \
    -DWITH_FFMPEG=ON \
    -DWITH_TBB=ON \
    -Wno-dev ../ && make -j32 install
ENV LD_LIBRARY_PATH /usr/local/lib:$LD_LIBRARY_PATH

WORKDIR /opt/nvidia
RUN mkdir installers

COPY cuda_7.5.18_linux.run /opt/nvidia/
RUN chmod +x cuda_7.5.18_linux.run && sync && ./cuda_7.5.18_linux.run -extract=`pwd`
COPY NVIDIA-Linux-x86_64-352.63.run /opt/nvidia/
RUN chmod +x NVIDIA-Linux-x86_64-352.63.run && sync && ./NVIDIA-Linux-x86_64-352.63.run -s -N --no-kernel-module
RUN ./cuda-linux64-rel-7.5.18-19867135.run -noprompt
RUN cd / && rm -rf /opt/nvidia
ENV PATH /usr/local/cuda/bin:$PATH
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64:$LD_LIBRARY_PATH

WORKDIR /usr/local
COPY cudnn-7.0-linux-x64-v3.0-prod.tgz /usr/local/
RUN tar zxvf cudnn-7.0-linux-x64-v3.0-prod.tgz
RUN rm -rf cudnn-7.0-linux-x64-v3.0-prod.tgz

COPY cvmodules /root/

WORKDIR /root/face
COPY caffe.tar.gz /root/face/
RUN tar zxvf caffe.tar.gz && rm -rf caffe.tar.gz
COPY cnn_age_gender_models_and_data.0.0.2.zip /root/face/
RUN unzip cnn_age_gender_models_and_data.0.0.2.zip
RUN rm -rf cnn_age_gender_models_and_data.0.0.2.zip
RUN cp /root/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml ./
RUN cd /root/face/caffe && mkdir build && cd build && cmake ../ && make -j32 install
RUN nohup python server.py &

WORKDIR /root/object
COPY fast-rcnn.tar.gz /root/object/
RUN tar zxvf fast-rcnn.tar.gz && rm -rf fast-rcnn.tar.gz
COPY dlib.tar.gz /root/object/
RUN tar zxvf dlib.tar.gz && rm -rf dlib.tar.gz
ENV FRCN_ROOT /root/object/fast-rcnn
RUN cd $FRCN_ROOT/lib && make
COPY fast_rcnn_models.tgz $FRCN_ROOT/data/
RUN cd $FRCN_ROOT/data && tar zxvf fast_rcnn_models.tgz && rm -rf fast_rcnn_models.tgz
RUN cd $FRCN_ROOT/caffe-fast-rcnn && mkdir build && cd build && cmake ../ && make -j32 install
RUN cd /root/object/dlib && python setup.py install
RUN nohup python server.py &

WORKDIR /root
CMD /root/anaconda2/bin/python /root/server.py
