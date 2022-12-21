# OS chosen
FROM debian:latest
LABEL maintainer="Alexvidalcor"

# Directory to use inside the container to prepare the application
WORKDIR /home/application

# All the files necessary for the application are copied
COPY ["requirements.txt", "main.py", "./"]
COPY ["src", "./src"]

# Install packages needed
RUN apt update \
    && apt install -y \
        python3-pip \
    && pip3 install -r \
        requirements.txt

# Run the command that initializes the app
CMD ["python3", "./main.py"]

