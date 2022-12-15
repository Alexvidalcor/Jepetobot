# Python libraries
import os
import random
from dotenv import load_dotenv

# Custom importation
import modules.public_env as penv
from modules.cdk_support import *

# Local secrets. Only run in your local.
if penv.execGithubActions == False:
    load_dotenv(".env")

# Variables from GithubSecrets/environment
try:

    # AWS variables
    awsAccount = os.environ["AWS_ACCOUNT"]
    awsRegion = os.environ["AWS_REGION"]
    awsTagName = os.environ["AWS_TAG_NAME"]

    # EC2 variables
    instanceName = os.environ["AWS_NAME_INSTANCE"]
    vpcId = os.environ["AWS_VPC_ID"]  # Import an Exist VPC
    ec2Type = "t3.micro"
    keyName = os.environ["AWS_KEY"]
    sgID = os.environ["AWS_SG"]

    # SecretManager variables
    awsSecret1 = os.environ["AWS_SECRET_1"]

    # Differentiate between local variables and Github actions
    if penv.execGithubActions:
        reusableStack = os.environ["REUSABLE_STACK"]
    else:
        reusableStack = penv.reusableStack

except KeyError:
    raise Exception("Are you using Github Secrets?")


# Extra variables. Only in local.
if reusableStack:
    timestamp = random.randint(0,999999)
else:
    timestamp = "managed"
