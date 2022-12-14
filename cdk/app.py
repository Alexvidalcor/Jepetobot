# AWS libraries
from aws_cdk import (
    App,
    Environment,
    Tags
)

# Python libraries
import random

# Stacks importation
from cdk_ec2.cdk_ec2_stack import Ec2Stack
from cdk_codedeploy.cdk_codedeploy_stack import CodeDeployStack
from cdk_s3.cdk_s3_stack import S3stack

# Python libraries
import os

# Custom importation. Only when running locally, emulate github actions inputs
import public_env as penv 

# Variables from Github Secrets
awsAccount = os.environ["AWS_ACCOUNT"]
awsRegion = os.environ["AWS_REGION"]
awsTagName = os.environ["AWS_TAG_NAME"]

# Differentiate between local variables and Github actions
if penv.execGithubActions:
    reusableStack = os.environ["REUSABLE_STACK"]
else:
    reusableStack = penv.reusableStack

# Extra variables. Only in local.
if reusableStack:
    timestamp = random.randint(0,999999)
else:
    timestamp = "managed"

# Set AWS environment
awsEnv = Environment(account=awsAccount, region=awsRegion)

# Execute stack
app = App()
Ec2Layer = Ec2Stack(app, f"cdk-ec2-deploy-{timestamp}", env=awsEnv)
CodeDeployLayer = CodeDeployStack(app, f"cdk-code-deploy-{timestamp}", env=awsEnv)
S3Layer = S3stack(app, f"cdk-s3-deploy-{timestamp}", env=awsEnv)

# Add tags
Tags.of(Ec2Layer).add("Group", awsTagName)
Tags.of(Ec2Layer).add("Name", awsTagName+"ec2")

Tags.of(CodeDeployLayer).add("Group", awsTagName)
Tags.of(CodeDeployLayer).add("Name", awsTagName+"codedeploy")

Tags.of(S3Layer).add("Group", awsTagName)
Tags.of(S3Layer).add("Name", awsTagName+"s3")


# Execute deploy
app.synth()
