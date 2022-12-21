#!/bin/bash

# Update the instance
yum update -y

# Set some environment vars
export AWS_DEFAULT_REGION=REPLACEREGION

# CodeDeploy agent installation 
yum install -y ruby wget
cd /home/ec2-user
wget https://aws-codedeploy-REPLACEREGION.s3.REPLACEREGION.amazonaws.com/latest/install
chmod +x ./install
./install auto
service codedeploy-agent start

# Docker installation
amazon-linux-extras install docker
service docker start
usermod -a -G docker ec2-user
systemctl enable docker
