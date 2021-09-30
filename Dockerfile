FROM debian:buster-slim
FROM python:3.9.7-slim-buster

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y nodejs \
    npm

RUN apt-get install git ffmpeg python3-pip -y
RUN pip3 install -U pip
RUN git clone http://github.com/satyanandatripathi/moosic /rikudo/bot

WORKDIR /rikudo/bot

RUN chmod 777 /rikudo/bot
RUN cd /rikudo/bot 

ENV PIP_NO_CACHE_DIR
RUN pip3 install --upgrade pip setuptools
RUN pip3 install --no-cache-dir -U -r requirements.txt

CMD ["python3", "-m", "Yukki"]
