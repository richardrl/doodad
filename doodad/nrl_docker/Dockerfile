# Use an official Python runtime as a parent image
FROM ubuntu:xenial
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get -y update && apt-get install -y --no-install-recommends apt-utils

# Set the working directory
ENV home=/home/ubuntu
WORKDIR $home
ADD . $home

RUN apt-get -y update && apt-get install -y python python-pip python-numpy python-dev cmake zlib1g-dev libjpeg-dev xvfb \
libav-tools xorg-dev python-opengl libboost-all-dev libsdl2-dev swig python3-dev \
make golang libjpeg-turbo8-dev gcc wget unzip git python-pygame
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
# RUN virtualenv curiosity
# RUN source $PWD/curiosity/bin/activate
RUN apt-get install -y tmux lsof
RUN pip install numpy six go_vncdriver
RUN pip install -r requirements.txt
RUN git clone https://github.com/openai/go-vncdriver.git
RUN ls
WORKDIR go-vncdriver
RUN python build.py #not ran
RUN pip install -e .
# install gym_ple, ple, pygame

# WORKDIR $home
# RUN git clone https://github.com/ntasfi/PyGame-Learning-Environment.git
# WORKDIR PyGame-Learning-Environment/
# RUN pip install -e .

# WORKDIR $home
# RUN git clone https://github.com/lusob/gym-ple.git
# WORKDIR gym-ple/
# RUN pip install -e .

WORKDIR $home

# Make port 22 available to the world outside this container
EXPOSE 22

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
# CMD ["python", "app.py"]
