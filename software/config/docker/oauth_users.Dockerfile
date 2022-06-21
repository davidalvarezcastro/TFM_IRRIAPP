FROM python:3

ARG LOGS_FOLDER

LABEL author = "davalv"

ENV TZ=Europe/Madrid

RUN mkdir -p /users
ADD ./server/auth/ /users/
ADD ./logs /users/logs
ADD ./.env /users/.env
WORKDIR /users
RUN python3 -m pip install -r /users/requirements.txt
RUN python3 -m pip install gunicorn
RUN python3 init_database.py

EXPOSE 5000
CMD  gunicorn -b 0.0.0.0:5000 wsgi:app
