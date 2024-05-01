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
awsRegion = os.environ["AWS_REGION"]
awsTagName = os.environ["AWS_TAG_NAME"]

# EC2 variables
sgPorts = eval(os.environ["AWS_SG_PORTS"]) # Must receive an array

# Github Actions variables 
envDeploy = os.environ["ENVIRONMENT_DEPLOY"]

# Custom variables
tz = os.environ["TZ"]
appName = os.environ["APP_NAME"]






