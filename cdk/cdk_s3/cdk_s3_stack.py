# AWS libraries
import public_env as penv
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    RemovalPolicy
)
from constructs import Construct

# Python libraries
import os
from dotenv import load_dotenv
import random

# Local secrets. Only run in your local.
if penv.execGithubActions == False:
    load_dotenv(".env")

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
