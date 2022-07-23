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
RUN pip install gunicorn

RUN mkdir /irrigation
RUN mkdir /logs
RUN chmod -R 777 /irrigation
RUN chmod -R 777 /logs

VOLUME "/irrigation"
VOLUME "/logs"
VOLUME /irrigation/$LOGS_FOLDER
WORKDIR /irrigation

EXPOSE 5000

CMD pip install -r requirements.txt && gunicorn -b 0.0.0.0:5000 wsgi:app
