# AWS libraries
from aws_cdk import (
    Stack,
    aws_secretsmanager as secretsmanager
)
from constructs import Construct

# Python libraries
import json

# Custom importation
from env.cdk_public_env import appName
from env.cdk_secrets_env import envDeploy

# MainClass
class SecretManagerStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # It stores default secrets
        secret1 = secretsmanager.Secret(self, 
        appName+ "-" + envDeploy + "_secret1",
        secret_name=appName + "-" + envDeploy + "_secret1",
        )

        # It stores random secrets
        secret2 = secretsmanager.Secret(self, 
        appName+ "-" + envDeploy + "_secret2",
        secret_name=appName + "-" + envDeploy + "_secret2",
        generate_secret_string=secretsmanager.SecretStringGenerator(
            secret_string_template=json.dumps({"App": appName + "-" + envDeploy}),
            generate_string_key="DB_KEY",
            generate_string_key="FILES_KEY"
        )

    )
