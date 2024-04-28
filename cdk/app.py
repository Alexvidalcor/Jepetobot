# AWS libraries
from aws_cdk import (
    App,
    Environment,
    Tags
)

# Custom importation
from env.cdk_public_env import appName
from env.cdk_secrets_env import envDeploy, awsRegion, awsAccount, awsTagName, reusableStack, random


# Stacks importation
from iac.ec2_stack import Ec2Stack
from iac.codedeploy_stack import CodeDeployStack
from iac.s3_stack import S3stack
from iac.secretmanager_stack import SecretManagerStack
from iac.cloudwatch_stack import CloudWatchStack
from iac.lambda1_stack import Lambda1Stack
from iac.lambda2_stack import Lambda2Stack


# Set AWS environment
awsEnv = Environment(account=awsAccount, region=awsRegion)

# Config deployment
if reusableStack == True:
    timestamp = random.randint(0,999999)
else:
    timestamp = "Managed"


# Execute stacks
app = App()

CodeDeployLayer = CodeDeployStack(app, f"{appName}-{envDeploy}--Codedeploy-stack-{timestamp}", env=awsEnv)

S3Layer = S3stack(app, f"{appName}-{envDeploy}--S3-stack-{timestamp}", env=awsEnv)

SecretManagerLayer = SecretManagerStack(app, f"{appName}-{envDeploy}--Secretmanager-stack-{timestamp}", env=awsEnv)

CloudWatchLayer = CloudWatchStack(app, f"{appName}-{envDeploy}--Cloudwatch-stack-{timestamp}", env=awsEnv)

Lambda1Layer = Lambda1Stack(app, f"{appName}-{envDeploy}--Lambda1-stack-{timestamp}", env=awsEnv)

Lambda2Layer = Lambda2Stack(app, f"{appName}-{envDeploy}--Lambda2-stack-{timestamp}", env=awsEnv)

Ec2Layer = Ec2Stack(app, f"{appName}-{envDeploy}--Ec2-stack-{timestamp}", env=awsEnv)


# Add tags

Tags.of(Ec2Layer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(Ec2Layer).add("Name", awsTagName + "-" + envDeploy + "_Ec2")

Tags.of(CodeDeployLayer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(CodeDeployLayer).add("Name", awsTagName + "-" + envDeploy + "_Codedeploy")

Tags.of(S3Layer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(S3Layer).add("Name", awsTagName + "-" + envDeploy + "_S3")

Tags.of(SecretManagerLayer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(SecretManagerLayer).add("Name", awsTagName + "-" + envDeploy + "_Secretmanager")

Tags.of(CloudWatchLayer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(CloudWatchLayer).add("Name", awsTagName + "-" + envDeploy + "_Cloudwatch")

Tags.of(Lambda1Layer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(Lambda1Layer).add("Name", awsTagName + "-" + envDeploy + "_Lambda1")

Tags.of(Lambda1Layer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(Lambda1Layer).add("Name", awsTagName + "-" + envDeploy + "_Lambda2")


# Execute deploy
app.synth()
