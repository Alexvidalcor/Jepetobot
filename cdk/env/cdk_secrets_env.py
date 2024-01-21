# Python libraries
import os
import random
from dotenv import load_dotenv


# Custom importation
from env.cdk_public_env import reusableStack


# Variables from GithubSecrets/LocalEnvironment

print("Using local env variables...")
load_dotenv("env/.cdk.env")

# AWS variables
awsAccount = os.environ["AWS_ACCOUNT"]
awsRegion = os.environ["AWS_REGION"]
awsTagName = os.environ["AWS_TAG_NAME"]

# EC2 variables
vpcId = os.environ["AWS_VPC_ID"]  # Import an Exist VPC
ec2Type = "t4g.nano"
sgID = os.environ["AWS_SG"]  # Import an Exist SG
sgPorts = eval(os.environ["AWS_SG_PORTS"]) # Must receive an array
ec2Key= os.environ["AWS_KEY"]

# Github Actions variables 
envDeploy = os.environ["ENVIRONMENT_DEPLOY"]

# Custom variables
tz = os.environ["TZ"]

try:
    reusableStack = (os.environ["REUSABLE_STACK"] == "true")
except KeyError:
    reusableStack = reusableStack






