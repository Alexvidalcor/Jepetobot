# AWS libraries
import public_env as penv
from aws_cdk import (
    Stack,
    aws_codedeploy as codedeploy
)
from constructs import Construct

# Python libraries
import os
from dotenv import load_dotenv

# Variables used
awsTagName = os.environ["AWS_TAG_NAME"]

# Local secrets. Only run in your local.
if penv.execGithubActions == False:
    load_dotenv(".env")


# Main Class
class CodeDeployStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        application = codedeploy.ServerApplication(self, penv.appName + "_app_codedeploy",application_name=penv.appName)

        deploymentGroup = codedeploy.ServerDeploymentGroup(
            self, penv.appName + "_group_codedeploy",
            application=application,
            deployment_group_name=f"{penv.appName}-deploygroup",
            install_agent=True,
            ec2_instance_tags=codedeploy.InstanceTagSet({
                "Group": [awsTagName],
                "Name": [awsTagName+"ec2"],
            })
        )
