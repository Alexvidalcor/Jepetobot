# AWS libraries
from aws_cdk import (
    Stack,
    aws_codedeploy as codedeploy
)
from constructs import Construct

# Custom importation
from modules.cdk_support import *

# Main Class


class CodeDeployStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        application = codedeploy.ServerApplication(self, appName + "-" + envDeploy + "_app_codedeploy", application_name=appName + "-" + envDeploy)

        deploymentGroup = codedeploy.ServerDeploymentGroup(
            self, appName + "-" + envDeploy + "_group_codedeploy",
            application=application,
            deployment_group_name=f"{appName}-{envDeploy}-deploygroup",
            install_agent=True,
            ec2_instance_tags=codedeploy.InstanceTagSet({
                "Group": [awsTagName + "-" + envDeploy],
                "Name": [appName + "-" + envDeploy +"-ec2"],
            })
        )
