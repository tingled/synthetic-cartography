FROM ubuntu:16.04

RUN apt-get update -y

RUN apt-get install -y \
    python3 \
    python3-dev \
    python3-pip \
    python3-numpy


RUN pip3 install --upgrade pip

ADD ./requirements.txt /workdir/
RUN pip3 install -r /workdir/requirements.txt
