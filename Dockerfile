# OS chosen
FROM debian:bookworm-slim AS installation-image
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

ARG timezone
ENV TZ=$timezone

ARG appName
ENV APP_NAME=$appName


# Set custom logs (only errors and app info)
RUN ln -sf /dev/stdout /home/application/src/logs/app.log \
    && ln -sf /dev/stderr /home/application/src/logs/errors.log


# Python virtualenv variables
ENV VIRTUAL_ENV=/opt/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


# Install packages needed
RUN apt update \
    && apt install -y \
        python3-pip \
        python3-venv \
        wkhtmltopdf \
    && python3 -m venv .venv $VIRTUAL_ENV \
    && pip install -r \
        requirements.txt


# Run the command that initializes the app
CMD ["python3", "./main.py"]

