FROM ubuntu:16.04

RUN apt-get update

# ffmpeg
RUN apt-get install -y ffmpeg

# install python stuff
RUN apt-get install -y \
    python3.5 \
    python3-pip \
    python3-numpy \
    python3-scipy

RUN pip3 install --upgrade pip
RUN pip3 install librosa
RUN pip3 install ipython
RUN pip3 install nose
