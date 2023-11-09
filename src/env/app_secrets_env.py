# AWS libraries
import botocore 
import botocore.session 
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig 

# Python libraries
import os
import json
from dotenv import load_dotenv

# Import modules
from src.env.app_public_env import appName


try:
    print("Using local env variables...")
    load_dotenv("src/env/.app.env")

    # Telegram variables
    idUsersAllowed = eval(os.environ["SECRET_USERS"])
    idAdminAllowed= eval(os.environ["SECRET_ADMINS"])

    # Token variables
    telegramToken = os.environ["SECRET_TELEGRAM"]
    openaiToken = os.environ["SECRET_OPENAI"]

    #Custom variables
    envDeploy = os.environ["ENVIRONMENT_DEPLOY"]
    awsRegion = os.environ["AWS_REGION"]

except KeyError:
    print("Failed!\nUsing secretmanager...")

    # Custom variables
    envDeploy = os.environ["ENVIRONMENT_DEPLOY"]
    awsRegion = os.environ["AWS_REGION"]

    # SecretManager connection
    session = botocore.session.Session()
    client = session.create_client('secretsmanager', region_name=awsRegion)
    cacheConfig = SecretCacheConfig()
    cache = SecretCache(config = cacheConfig, client = client)

    # Telegram variables
    secret1 = cache.get_secret_string(appName + "-" + envDeploy + "_secret1")
    telegramToken = json.loads(secret1)["secret_telegram"]

    # OpenAI variables
    secret2 = cache.get_secret_string(appName + "-" + envDeploy + "_secret1")
    openaiToken = json.loads(secret1)["secret_openai"]

    # UsersFirewall variables
    secret3 = cache.get_secret_string(appName + "-" + envDeploy + "_secret1")
    idUsersAllowed = eval(json.loads(secret1)["secret_users"])

    # AdminFirewall variables
    secret3 = cache.get_secret_string(appName + "-" + envDeploy + "_secret1")
    idAdminAllowed = eval(json.loads(secret1)["secret_admins"])
