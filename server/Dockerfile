# base image
FROM --platform=linux/amd64 lorifranke/autorlx-base:0.1.0
#RUN apt update
#RUN apt install -y software-properties-common
#RUN add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) universe"
#RUN apt update
#RUN apt install -y supervisor

# install mushroom-rl
WORKDIR /usr/src/app
RUN git clone https://github.com/lorifranke/mushroom-rl.git
WORKDIR /usr/src/app/mushroom-rl
RUN pip install .

# install arlo
WORKDIR /usr/src/app
RUN git clone https://github.com/lorifranke/arlo.git
WORKDIR /usr/src/app/arlo
RUN pip install .
RUN mkdir logs

# install autorlx
WORKDIR /usr/src/app
COPY setup.py .
RUN pip install .
COPY . .

EXPOSE 8000
ENV OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# start supervisor
# RUN pip install supervisor==3.3.1
# ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# CMD [ "/usr/bin/supervisord" ]
CMD ["python", "main.py"]
