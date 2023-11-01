# AWS libraries
from aws_cdk import (
    App,
    Environment,
    Tags
)

# Custom importation
from env.cdk_support import *

# Stacks importation
from cdk_ec2.cdk_ec2_stack import Ec2Stack
from cdk_codedeploy.cdk_codedeploy_stack import CodeDeployStack
from cdk_s3.cdk_s3_stack import S3stack
from cdk_secretmanager.cdk_secretmanager_stack import SecretManagerStack
from cdk_cloudwatch.cdk_cloudwatch_stack import CloudWatchStack
from cdk_lambda.cdk_lambda1_stack import Lambda1Stack
from cdk_lambda.cdk_lambda2_stack import Lambda2Stack

# Set AWS environment
awsEnv = Environment(account=awsAccount, region=awsRegion)

# Execute stacks
app = App()
Ec2Layer = Ec2Stack(app, f"{appName}-{envDeploy}--ec2-stack-{timestamp}", env=awsEnv)
CodeDeployLayer = CodeDeployStack(app, f"{appName}-{envDeploy}--codedeploy-stack-{timestamp}", env=awsEnv)
S3Layer = S3stack(app, f"{appName}-{envDeploy}--s3-stack-{timestamp}", env=awsEnv)
SecretManagerLayer = SecretManagerStack(app, f"{appName}-{envDeploy}--secretmanager-stack-{timestamp}", env=awsEnv)
CloudWatchLayer = CloudWatchStack(app, f"{appName}-{envDeploy}--cloudwatch-stack-{timestamp}", env=awsEnv)
Lambda1Layer = Lambda1Stack(app, f"{appName}-{envDeploy}--lambda1-stack-{timestamp}", env=awsEnv)
Lambda2Layer = Lambda2Stack(app, f"{appName}-{envDeploy}--lambda2-stack-{timestamp}", env=awsEnv)


# Add tags
Tags.of(Ec2Layer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(Ec2Layer).add("Name", awsTagName + "-" + envDeploy + "-ec2")

Tags.of(CodeDeployLayer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(CodeDeployLayer).add("Name", awsTagName + "-" + envDeploy + "-codedeploy")

Tags.of(S3Layer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(S3Layer).add("Name", awsTagName + "-" + envDeploy + "-s3")

Tags.of(SecretManagerLayer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(SecretManagerLayer).add("Name", awsTagName + "-" + envDeploy + "-secretmanager")

Tags.of(CloudWatchLayer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(CloudWatchLayer).add("Name", awsTagName + "-" + envDeploy + "-cloudwatch")

Tags.of(Lambda1Layer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(Lambda1Layer).add("Name", awsTagName + "-" + envDeploy + "-lambda1")

Tags.of(Lambda1Layer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(Lambda1Layer).add("Name", awsTagName + "-" + envDeploy + "-lambda2")

# Execute deploy
app.synth()
