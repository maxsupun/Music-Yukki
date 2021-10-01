FROM debian:buster-slim
FROM python:3.9.7-slim-buster


RUN apt-get update -y && apt-get upgrade -y && \
RUN curl -sL https://deb.nodesource.com/setup_15.x | bash -
RUN apt-get install -y nodejs \
    npm


RUN apt-get install git ffmpeg python3-pip -y
RUN pip3 install -U pip
RUN git clone http://github.com/levina-lab/vmusic /veez/bot

WORKDIR /veez/bot

RUN chmod 777 /veez/bot
RUN cd /veez/bot 

ENV PIP_NO_CACHE_DIR 1
RUN pip3 install --upgrade pip setuptools
RUN pip3 install --no-cache-dir -U -r requirements.txt
RUN pip3 uninstall pytgcalls && pip3 install git+https://github.com/pyrogram/pyrogram -U && pip3 uninstall py-tgcalls && pip3 install py-tgcalls==0.5.5 && pip3 install lyricsgenius && pip3 install hachoir


CMD ["python3", "-m", "Yukki"]
