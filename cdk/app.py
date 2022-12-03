# #AWS libraries
from aws_cdk import App, Environment, Tags
from cdk_vpc_ec2.cdk_vpc_ec2_stack import CdkVpcEc2Stack

# Python libraries
import os

# Variables from Github Secrets
awsAccount = os.environ("AWS_ACCOUNT")
awsRegion = os.environ("AWS_REGION")
awsTagGroupName = os.environ("AWS_TAG_GROUP_NAME")
awsTagName = os.environ("AWS_TAG_NAME")

# Set 
awsEnv = Environment(account= awsAccount, region=awsRegion)

app = App()
CdkVpcEc2Stack(app, "cdk-vpc-ec2", env=awsEnv)

Tags.of(CdkVpcEc2Stack).add("Group", "group_name").add(awsTagGroupName , awsTagName)

app.synth()
