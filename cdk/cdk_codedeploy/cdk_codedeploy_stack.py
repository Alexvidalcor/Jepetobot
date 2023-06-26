# AWS libraries
from aws_cdk import (
    Stack,
    aws_codedeploy as codedeploy
)
from constructs import Construct

# Custom importation
from env.cdk_support import *

# Main Class


class CodeDeployStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        application = codedeploy.ServerApplication(self, appName + "-" + envDeploy + "_app-codedeploy", application_name=appName + "-" + envDeploy + "_app-codedeploy")

        deploymentGroup = codedeploy.ServerDeploymentGroup(
            self, appName + "-" + envDeploy + "_group-codedeploy",
            application=application,
            deployment_group_name=f"{appName}-{envDeploy}_group-codedeploy",
            install_agent=True,
            ec2_instance_tags=codedeploy.InstanceTagSet({
                "Group": [awsTagName + "-" + envDeploy],
                "Name": [appName + "-" + envDeploy +"_ec2"],
            })
        )
