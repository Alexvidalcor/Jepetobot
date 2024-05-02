# AWS libraries
from aws_cdk import (
    App,
    Environment,
    Tags
)

# Custom importation
from env.cdk_secrets_env import envDeploy, awsRegion, awsAccount, appName, appName


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


# Execute stacks
app = App()

CodeDeployLayer = CodeDeployStack(app, f"{appName}-{envDeploy}--Cdk-codedeploystack", env=awsEnv)

S3Layer = S3stack(app, f"{appName}-{envDeploy}--Cdk-s3stack", env=awsEnv)

SecretManagerLayer = SecretManagerStack(app, f"{appName}-{envDeploy}--Cdk-secretmanagerstack", env=awsEnv)

CloudWatchLayer = CloudWatchStack(app, f"{appName}-{envDeploy}--Cdk-cloudwatchstack", env=awsEnv)

LambdaLayer1 = Lambda1Stack(app, f"{appName}-{envDeploy}--Cdk-lambdastack1", env=awsEnv)

LambdaLayer2 = Lambda2Stack(app, f"{appName}-{envDeploy}--Cdk-lambdastack2", env=awsEnv)

Ec2Layer = Ec2Stack(app, f"{appName}-{envDeploy}--Cdk-ec2stack", env=awsEnv)


# Add tags

Tags.of(Ec2Layer).add("Group", appName + "-" + envDeploy)
Tags.of(Ec2Layer).add("Name", appName + "-" + envDeploy + "_Ec2")

Tags.of(CodeDeployLayer).add("Group", appName + "-" + envDeploy)
Tags.of(CodeDeployLayer).add("Name", appName + "-" + envDeploy + "_Codedeploy")

Tags.of(S3Layer).add("Group", appName + "-" + envDeploy)
Tags.of(S3Layer).add("Name", appName + "-" + envDeploy + "_S3")

Tags.of(SecretManagerLayer).add("Group", appName + "-" + envDeploy)
Tags.of(SecretManagerLayer).add("Name", appName + "-" + envDeploy + "_Secretmanager")

Tags.of(CloudWatchLayer).add("Group", appName + "-" + envDeploy)
Tags.of(CloudWatchLayer).add("Name", appName + "-" + envDeploy + "_Cloudwatch")

Tags.of(Lambda1Layer).add("Group", appName + "-" + envDeploy)
Tags.of(Lambda1Layer).add("Name", appName + "-" + envDeploy + "_Lambda1")

Tags.of(Lambda1Layer).add("Group", appName + "-" + envDeploy)
Tags.of(Lambda1Layer).add("Name", appName + "-" + envDeploy + "_Lambda2")


# Execute deploy
app.synth()
