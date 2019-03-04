FROM python:latest

WORKDIR /usr/src/app

RUN pip install paho-mqtt
RUN pip install watchdog

RUN mkdir clonewar

COPY clone_war.py .
RUN chmod 777 clone_war.py

CMD [ "python", "./clone_war.py" ]