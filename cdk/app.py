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

codedeployLayer = CodeDeployStack(app, f"{appName}-{envDeploy}--Cdk-codedeploystack", env=awsEnv)

s3Layer = S3stack(app, f"{appName}-{envDeploy}--Cdk-s3stack", env=awsEnv)

secretmanagerLayer = SecretManagerStack(app, f"{appName}-{envDeploy}--Cdk-secretmanagerstack", env=awsEnv)

cloudwatchLayer = CloudWatchStack(app, f"{appName}-{envDeploy}--Cdk-cloudwatchstack", env=awsEnv)

lambdaLayer1 = Lambda1Stack(app, f"{appName}-{envDeploy}--Cdk-lambdastack1", env=awsEnv)

lambdaLayer2 = Lambda2Stack(app, f"{appName}-{envDeploy}--Cdk-lambdastack2", env=awsEnv)

ec2Layer = Ec2Stack(app, f"{appName}-{envDeploy}--Cdk-ec2stack", env=awsEnv)


# Add tags

Tags.of(ec2Layer).add("Group", appName + "-" + envDeploy)
Tags.of(ec2Layer).add("Name", appName + "-" + envDeploy + "_Ec2")

Tags.of(codedeployLayer).add("Group", appName + "-" + envDeploy)
Tags.of(codedeployLayer).add("Name", appName + "-" + envDeploy + "_Codedeploy")

Tags.of(s3Layer).add("Group", appName + "-" + envDeploy)
Tags.of(s3Layer).add("Name", appName + "-" + envDeploy + "_S3")

Tags.of(secretmanagerLayer).add("Group", appName + "-" + envDeploy)
Tags.of(secretmanagerLayer).add("Name", appName + "-" + envDeploy + "_Secretmanager")

Tags.of(cloudwatchLayer).add("Group", appName + "-" + envDeploy)
Tags.of(cloudwatchLayer).add("Name", appName + "-" + envDeploy + "_Cloudwatch")

Tags.of(lambdaLayer1).add("Group", appName + "-" + envDeploy)
Tags.of(lambdaLayer1).add("Name", appName + "-" + envDeploy + "_Lambda1")

Tags.of(lambdaLayer2).add("Group", appName + "-" + envDeploy)
Tags.of(lambdaLayer2).add("Name", appName + "-" + envDeploy + "_Lambda2")


# Execute deploy
app.synth()
