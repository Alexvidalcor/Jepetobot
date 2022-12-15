# AWS libraries
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    RemovalPolicy
)
from constructs import Construct

# Python libraries
import random

# Custom importation
import modules.public_env as penv
from modules.cdk_support import *

# MainClass
class S3stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket(self, penv.appName + "_s3-bucket",
                            bucket_name=(f"cdk-s3-{penv.appName.lower()}-{random.randint(0,99)}-{random.randint(0,99)}"),
                            auto_delete_objects=True,
                            removal_policy=RemovalPolicy.DESTROY,
                            block_public_access=s3.BlockPublicAccess.BLOCK_ALL 
                            )
