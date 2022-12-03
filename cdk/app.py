# #AWS libraries
from aws_cdk import (
    App, 
    Environment, 
    Tags
)

# Python libraries
import os

# Variables from Github Secrets
awsAccount = os.environ["AWS_ACCOUNT"]
awsRegion = os.environ["AWS_REGION"]
awsTagGroupName = os.environ["AWS_TAG_GROUP_NAME"]
awsTagName = os.environ["AWS_TAG_NAME"]

# Set AWS environment
awsEnv = Environment(account= awsAccount, region=awsRegion)

# Execute stack
app = App()
EC2InstanceStack(app, "cdk_ec2", env=awsEnv)


# Add tags
Tags.of(EC2InstanceStack).add("Group", "group_name").add(awsTagGroupName , awsTagName)

# Execute deploy
app.synth()
