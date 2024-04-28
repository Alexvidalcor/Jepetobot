# AWS libraries
from aws_cdk import (
    Stack,
    aws_iam as iam
)
from constructs import Construct

# Custom importation
from env.cdk_public_env import  appName
from env.cdk_secrets_env import envDeploy


class IamStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create IAM group
        iam_group1 = iam.Group(self, appName + "-" + envDeploy + "_Iam-group1",group_name=appName + "-" + envDeploy + "_Iam-group1")

        # Ec2 permissions
        iam_group1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonEC2FullAccess"
            )
        )

        # S3 permissions
        iam_group1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3FullAccess"
            )
        )

        # Cloudformation permissions
        iam_group1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AWSCloudFormationFullAccess"
            )
        )

        # Secretmanager permissions
        iam_group1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "SecretsManagerReadWrite"
            )
        )

        # Lambda permissions
        iam_group1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AWSLambda_FullAccess"
            )
        )

        # Cloudwatch permissions
        iam_group1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "CloudWatchEventsFullAccess"
            )
        )

        # Codedeploy permissions
        iam_group1.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AWSCodeDeployFullAccess"
            )
        )

        # Create user in the group created before
        iam_user1 = iam.User(self, appName + "-" + envDeploy + "_Iam-user1", user_name=appName + "-" + envDeploy + "_Iam-user1")
        iam_user1.add_to_group(iam_group1)
