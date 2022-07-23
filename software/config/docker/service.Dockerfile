FROM python:3.8

LABEL author = "davalv"

ENV TZ=Europe/Madrid

ARG LOGS_FOLDER
ARG SERVICE_FILE
ENV SERVICE_FILE ${SERVICE_FILE}

RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade
RUN apt-get install -y \
  build-essential \
  python3 \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip

RUN mkdir /irrigation
RUN mkdir /logs
RUN chmod -R 777 /irrigation
RUN chmod -R 777 /logs

VOLUME "/irrigation"
VOLUME /irrigation/$LOGS_FOLDER
WORKDIR /irrigation

CMD pip install -r requirements.txt && cp ${SERVICE_FILE} main.py && python main.py
