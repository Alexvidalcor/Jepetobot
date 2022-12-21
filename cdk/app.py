# AWS libraries
from aws_cdk import (
    App,
    Environment,
    Tags
)

# Custom importation
from modules.cdk_support import *

# Stacks importation
from cdk_ec2.cdk_ec2_stack import Ec2Stack
from cdk_codedeploy.cdk_codedeploy_stack import CodeDeployStack
from cdk_s3.cdk_s3_stack import S3stack
from cdk_secretmanager.cdk_secretmanager_stack import SecretManagerStack

# Set AWS environment
awsEnv = Environment(account=awsAccount, region=awsRegion)

# Execute stacks
app = App()
Ec2Layer = Ec2Stack(app, f"cdk-ec2-stack-{timestamp}", env=awsEnv)
CodeDeployLayer = CodeDeployStack(app, f"cdk-codedeploy-stack-{timestamp}", env=awsEnv)
S3Layer = S3stack(app, f"cdk-s3-stack-{timestamp}", env=awsEnv)
SecretManagerLayer = SecretManagerStack(app, f"cdk-secretmanager-stack-{timestamp}", env=awsEnv)

# Add tags
Tags.of(Ec2Layer).add("Group", awsTagName)
Tags.of(Ec2Layer).add("Name", awsTagName+"-ec2")

Tags.of(CodeDeployLayer).add("Group", awsTagName)
Tags.of(CodeDeployLayer).add("Name", awsTagName+"-codedeploy")

Tags.of(S3Layer).add("Group", awsTagName)
Tags.of(S3Layer).add("Name", awsTagName+"-s3")

Tags.of(SecretManagerLayer).add("Group", awsTagName)
Tags.of(SecretManagerLayer).add("Name", awsTagName+"-secretmanager")

# Execute deploy
app.synth()
