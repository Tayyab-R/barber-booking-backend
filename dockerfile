FROM python:3.14-rc-alpine3.21

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apk add postgresql-dev

COPY requirements.txt $DJANGODIRECTORY
RUN pip install -r requirements.txt    

COPY wait-for-it.sh $DJANGODIRECTORY
RUN apk add --no-cache bash

ARG USER=user
ARG DJANGODIRECTORY=/usr/src/app
ARG UID=1141

ENV USER=$USER
ENV DJANGODIRECTORY=$DJANGODIRECTORY
ENV USERID=$UID

WORKDIR $DJANGODIRECTORY

COPY . $DJANGODIRECTORY

RUN adduser -s /bin/sh -D -u $UID $USER && \
    chown -R $USER:$USER $DJANGODIRECTORY && \
    chmod +x $DJANGODIRECTORY/wait-for-it.sh

EXPOSE 8000

