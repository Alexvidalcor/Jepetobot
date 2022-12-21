# Python libraries
import os
import random
from dotenv import load_dotenv

# Custom importation
import modules.cdk_public_env as penv

# Local secrets. Only run in your local.
if penv.execLocal:
    print("Using local env variables...")
    load_dotenv("modules/.env")

# Variables from GithubSecrets/environment
try:

    # AWS variables
    awsAccount = os.environ["AWS_ACCOUNT"]
    awsRegion = os.environ["AWS_DEFAULT_REGION"]
    awsTagName = os.environ["AWS_TAG_NAME"]

    # EC2 variables
    instanceName = os.environ["AWS_NAME_INSTANCE"]
    vpcId = os.environ["AWS_VPC_ID"]  # Import an Exist VPC
    ec2Type = "t3.micro"
    keyName = os.environ["AWS_KEY"]
    sgID = os.environ["AWS_SG"]

    # Public_env variables
    appName = penv.appName
    showPublicIp = penv.showPublicIp

    # Differentiate between local variables and Github actions variables
    if penv.execLocal == False:
        reusableStack = os.environ["REUSABLE_STACK"]
    else:
        reusableStack = penv.reusableStack

except KeyError:
    raise Exception("Are you using Github Secrets? Check cdk_public_env file")

# Extra variables. Only in local.
if reusableStack:
    timestamp = random.randint(0,999999)
else:
    timestamp = "managed"
