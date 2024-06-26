# AWS libraries
from aws_cdk import (
    Stack,
    Duration,
    aws_s3 as s3,
    RemovalPolicy
)
from constructs import Construct

# Python libraries
import random

# Custom importation
from env.cdk_secrets_env import envDeploy, appName

# MainClass
class S3stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket(self, appName + "-" + envDeploy + "_S3-bucket",
                            bucket_name = (f"{appName.lower()}-{envDeploy.lower()}--s3-bucket-{random.randint(0,99)}-{random.randint(0,99)}"),
                            auto_delete_objects=True,
                            removal_policy=RemovalPolicy.DESTROY,
                            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                            lifecycle_rules=[
                                s3.LifecycleRule(
                                enabled=True,
                                expiration=Duration.days(15),
                            )
                        ] 
                    )
