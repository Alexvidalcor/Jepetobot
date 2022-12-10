# AWS libraries
from aws_cdk import (
    App,
    Environment,
    Tags
)

# Python libraries
from datetime import datetime

# Stack importation
from cdk_ec2.cdk_ec2_stack import EC2InstanceStack

# Python libraries
import os

# Custom importation. Only when running locally, emulate github actions inputs
import public_env as penv 

# Variables from Github Secrets
awsAccount = os.environ["AWS_ACCOUNT"]
awsRegion = os.environ["AWS_REGION"]
awsTagGroupName = os.environ["AWS_TAG_GROUP_NAME"]
awsTagName = os.environ["AWS_TAG_NAME"]

# Differentiate between local variables and Github actions
if penv.execGithubActions:
    reusableStack = os.environ["REUSABLE_STACK"]
else:
    reusableStack = penv.reusableStack

# Extra variables. Only in local.
if reusableStack:
    timestamp = datetime.fromtimestamp(1887639468)
else:
    timestamp = "managed"

# Set AWS environment
awsEnv = Environment(account=awsAccount, region=awsRegion)

# Execute stack
app = App()
EC2InstanceLayer = EC2InstanceStack(app, f"cdk-ec2-deploy-{timestamp}", env=awsEnv)

# Add tags
Tags.of(EC2InstanceLayer).add("Group", awsTagGroupName)
Tags.of(EC2InstanceLayer).add("Name", awsTagName)

# Execute deploy
app.synth()
