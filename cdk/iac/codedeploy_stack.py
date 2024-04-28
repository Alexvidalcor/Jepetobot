# AWS libraries
from aws_cdk import (
    Stack,
    aws_codedeploy as codedeploy
)
from constructs import Construct

# Custom importation
from env.cdk_public_env import appName
from env.cdk_secrets_env import envDeploy, awsTagName


# Main Class
class CodeDeployStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        application = codedeploy.ServerApplication(self, appName + "-" + envDeploy + "_Codedeploy-app", application_name=appName + "-" + envDeploy + "_Codedeploy-app")

        deploymentGroup = codedeploy.ServerDeploymentGroup(
            self, appName + "-" + envDeploy + "_Codedeploy-group",
            application=application,
            deployment_group_name=f"{appName}-{envDeploy}_Codedeploy-group",
            install_agent=True,
            ec2_instance_tags=codedeploy.InstanceTagSet({
                "Group": [awsTagName + "-" + envDeploy],
                "Name": [appName + "-" + envDeploy +"_Ec2"],
            })
        )
