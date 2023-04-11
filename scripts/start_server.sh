#!/bin/bash

docker run -d -it --name app_cont -v /var/log/application:/home/application/src/logs --restart always app_image
