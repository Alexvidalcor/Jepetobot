# #AWS libraries
from aws_cdk import App, Environment, Tags, aws_ec2

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
aws_ec2(app, "cdk_ec2", env=awsEnv)


# Add tags
Tags.of(aws_ec2).add("Group", "group_name").add(awsTagGroupName , awsTagName)

# Execute deploy
app.synth()
