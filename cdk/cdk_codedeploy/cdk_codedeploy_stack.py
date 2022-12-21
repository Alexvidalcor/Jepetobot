# AWS libraries
from aws_cdk import (
    Stack,
    aws_codedeploy as codedeploy
)
from constructs import Construct

# Custom importation
import modules.public_env as penv
from modules.cdk_support import *

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
                "Name": [awsTagName+"-ec2"],
            })
        )
