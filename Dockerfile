FROM debian:latest
LABEL maintainer="Alexvidalcor"

RUN apt update \
    && apt install -y \
        python3-pip \
        firefox-esr \
    && pip install \
        selenium \
        webdriver-manager \
        python-telegram-bot