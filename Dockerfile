FROM debian:latest
LABEL maintainer="Alexvidalcor"

WORKDIR /home/application
COPY ["requirements.txt", "main.py", "src"]

RUN apt update \
    && apt install -y \
        python3-pip \
    && pip install -r \
        requirements.txt

