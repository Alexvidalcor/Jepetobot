FROM debian:latest
LABEL maintainer="Alexvidalcor"

RUN apt update \
    && apt install -y \
        python3-pip \
    && pip install \
        python-telegram-bot