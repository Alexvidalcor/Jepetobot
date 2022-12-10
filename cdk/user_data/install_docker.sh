'''
Shebang is added automatically
You dont need to use sudo inside user data.
'''
#! /bin/sh
yum update -y
amazon-linux-extras install docker
service docker start
usermod -a -G docker ec2-user
systemctl enable docker