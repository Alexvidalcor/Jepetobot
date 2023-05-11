#!/bin/bash

cd /home/ec2-user/application
docker build --build-arg awsRegionDocker=$AWS_DEFAULT_REGION --build-arg envDeploy=$ENVIRONMENT_DEPLOY -t app_image  .
