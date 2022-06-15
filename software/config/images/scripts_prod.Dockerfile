FROM python:3.8

LABEL author = "davalv"

ENV TZ=Europe/Madrid

ARG LOGS_FOLDER

RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade
RUN apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
&& rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip

RUN mkdir /src
RUN mkdir -p /src/app
RUN chmod 777 /src
RUN chmod -R 777 /src

VOLUME "/src"
VOLUME "/src/app"
VOLUME /users/$LOGS_FOLDER
WORKDIR /src

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python3 main.py
