# AWS libraries
from aws_cdk import (
    Stack,
    aws_secretsmanager as secretsmanager
)
from constructs import Construct

# Python libraries
import json

# Custom importation
import modules.public_env as penv
from modules.cdk_support import *

# MainClass
class SecretManagerStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Default secret
        secret1 = secretsmanager.Secret(self, 
        penv.appName+"_secret1",
        secret_name=penv.appName+"_secret1",
        generate_secret_string=secretsmanager.SecretStringGenerator(
            secret_string_template=json.dumps({"App": penv.appName}),
            generate_string_key="password"
        )
    )
