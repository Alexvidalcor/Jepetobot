#!/bin/bash

if [ $( docker ps -a | grep app_cont | wc -l ) -gt 0 ]; then
    echo "app_cont exists"
    docker stop app_cont
    docker rm app_cont
    docker rmi app_image
else
        echo "app_cont does not exist"
fi
