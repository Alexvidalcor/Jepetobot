#!/bin/bash

cd /home/ec2-user/application
docker build --build-arg awsRegionDocker=$AWS_REGION --build-arg envDeploy=$ENVIRONMENT_DEPLOY --build-arg appName=$APP_NAME --build-arg timezone=$TZ -t app_image  .
