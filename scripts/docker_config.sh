#!/bin/bash

cd /home/ec2-user/application
docker build --build-arg awsRegionDocker=$AWS_DEFAULT_REGION -t app_image  .
