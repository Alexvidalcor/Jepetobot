#!/bin/bash

# Update the instance
yum update -y

# Set some environment vars
echo export AWS_REGION=REPLACEREGION >> /etc/profile
echo export ENVIRONMENT_DEPLOY=REPLACEENVNAME >> /etc/profile
echo export TZ=REPLACETZ >> /etc/profile 

# CodeDeploy agent installation 
yum install -y ruby wget
cd /home/ec2-user
wget https://aws-codedeploy-REPLACEREGION.s3.REPLACEREGION.amazonaws.com/latest/install
chmod +x ./install
./install auto
service codedeploy-agent start

# Cloudwatch agent installation
yum install -y amazon-cloudwatch-agent

# Docker installation
amazon-linux-extras install docker
service docker start
usermod -a -G docker ec2-user
systemctl enable docker
