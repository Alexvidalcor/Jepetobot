# Python libraries
import os
import random
from dotenv import load_dotenv


# Variables from GithubSecrets/LocalEnvironment

print("Using local env variables...")
load_dotenv("env/.cdk.env")

# AWS variables
awsRegion = os.environ["AWS_REGION"]
awsAccount = os.environ["AWS_ACCOUNT"]

# EC2 variables
sgPorts = eval(os.environ["AWS_SGPORTS"]) # Must receive an array

# Github Actions variables 
envDeploy = os.environ["ENVIRONMENT_DEPLOY"]

# Custom variables
tz = os.environ["GENERIC_TZ"]
appName = os.environ["APP_NAME"]






