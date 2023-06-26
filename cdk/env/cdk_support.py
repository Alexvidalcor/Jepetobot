# Python libraries
import os
import random
from dotenv import load_dotenv

# Custom importation
import env.cdk_public_env as penv

# Local secrets. Only run in your local.
if penv.execLocal:
    print("Using local env variables...")
    load_dotenv("env/.cdk_env")

# Variables from GithubSecrets/environment
try:

    # AWS variables
    awsAccount = os.environ["AWS_ACCOUNT"]
    awsRegion = os.environ["AWS_REGION"]
    awsTagName = os.environ["AWS_TAG_NAME"]

    # EC2 variables
    vpcId = os.environ["AWS_VPC_ID"]  # Import an Exist VPC
    ec2Type = "t3.nano"
    sgID = os.environ["AWS_SG"]  # Import an Exist SG
    sgPorts = eval(os.environ["AWS_SG_PORTS"]) # Must receive an array

    # Github Actions variables 
    envDeploy = os.environ["ENVIRONMENT_DEPLOY"]

    # Public_env variables
    appName = penv.appName
    showPublicIp = penv.showPublicIp
    createSG = penv.createSG

    # Differentiate between local variables and Github actions variables
    if penv.execLocal == False:
        reusableStack = (os.environ["REUSABLE_STACK"] == "true")
    else:
        reusableStack = penv.reusableStack

except KeyError:
    raise Exception("Are you using Github Secrets? Check cdk_public_env file")

# Extra variables. Only in local.
if reusableStack == True:
    timestamp = random.randint(0,999999)
else:
    timestamp = "managed"
