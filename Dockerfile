FROM debian:latest
LABEL maintainer="Alexvidalcor"

WORKDIR /home/application
COPY ["requirements.txt", "main.py", "src", "./"]

RUN apt update \
    && apt install -y \
        python3-pip \
    && pip3 install -r \
        requirements.txt

CMD ["python3", "./main.py"]

