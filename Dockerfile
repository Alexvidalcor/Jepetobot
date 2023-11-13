# OS chosen
FROM debian:bullseye-slim
LABEL maintainer="Alexvidalcor"

# Directory to use inside the container to prepare the application
WORKDIR /home/application

# All the files necessary for the application are copied
COPY ["requirements.txt", "main.py", "./"]
COPY ["src", "./src"]

# Set some environment vars
ARG awsRegionDocker
ENV AWS_REGION=$awsRegionDocker

ARG envDeploy
ENV ENVIRONMENT_DEPLOY=$envDeploy

# Set custom logs (only errors and app info)
RUN ln -sf /dev/stdout /home/application/src/logs/app.log \
    && ln -sf /dev/stderr /home/application/src/logs/errors.log

# Install packages needed
RUN apt update \
    && apt install -y \
        python3-pip \
    && pip3 install -r \
        requirements.txt

# Run the command that initializes the app
CMD ["python3", "./main.py"]

