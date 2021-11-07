FROM python:3.10.0-slim-buster
RUN apt update && apt upgrade -y
RUN apt install git curl python3-pip ffmpeg -y
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt install -y nodejs
RUN npm i -g npm@latest
COPY . /app
WORKDIR /app
RUN pip3 install -U pip
RUN pip3 install -U -r requirements.txt
CMD python3 -m Yukki
