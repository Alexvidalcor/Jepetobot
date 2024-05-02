# AWS libraries
from aws_cdk import (
    Stack,
    aws_iam as iam
)
from constructs import Construct

# Custom importation
from env.cdk_secrets_env import envDeploy, appName


class IamStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create IAM group
        iamGroup1 = iam.Group(self, appName + "-" + envDeploy + "_Iam-group1",group_name=appName + "-" + envDeploy + "_Iam-group1")

        # Ec2 permissions
        iamGroup1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonEC2FullAccess"
            )
        )

        # S3 permissions
        iamGroup1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3FullAccess"
            )
        )

        # Cloudformation permissions
        iamGroup1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AWSCloudFormationFullAccess"
            )
        )

        # Secretmanager permissions
        iamGroup1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "SecretsManagerReadWrite"
            )
        )

        # Lambda permissions
        iamGroup1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AWSLambda_FullAccess"
            )
        )

        # Cloudwatch permissions
        iamGroup1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "CloudWatchEventsFullAccess"
            )
        )

        # Codedeploy permissions
        iamGroup1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AWSCodeDeployFullAccess"
            )
        )

        # Create user in the group created before
        iamUser1 = iam.User(self, appName + "-" + envDeploy + "_Iam-user1", user_name=appName + "-" + envDeploy + "_Iam-user1")
        iamUser1.add_to_group(iamGroup1)
