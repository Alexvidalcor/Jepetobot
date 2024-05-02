#!/bin/bash

# Update the instance
dnf update -y

# Set some environment vars
echo export AWS_REGION=REPLACEREGION >> /etc/profile
echo export ENVIRONMENT_DEPLOY=REPLACEENVNAME >> /etc/profile
echo export TZ=REPLACETZ >> /etc/profile
echo export APP_NAME=REPLACEAPPNAME >> /etc/profile 

# CodeDeploy agent installation 
dnf install -y ruby wget
cd /home/ec2-user
wget https://aws-codedeploy-REPLACEREGION.s3.REPLACEREGION.amazonaws.com/latest/install
chmod +x ./install
./install auto
service codedeploy-agent start

# Cloudwatch agent installation
dnf install -y amazon-cloudwatch-agent

# Docker installation
dnf install docker
usermod -a -G docker ec2-user
newgrp docker
systemctl start docker
systemctl enable docker
