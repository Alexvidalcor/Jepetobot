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

# Variables from GithubSecrets/environment
try:
    print("Using local env secrets...")
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
    dbKey = os.environ["DB_KEY"]
    fileKey = os.environ["FILE_KEY"]

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

    # Telegram secret
    secret1 = cache.get_secret_string(appName + "-" + envDeploy + "_secret1")
    telegramToken = json.loads(secret1)["secret_telegram"]

    # OpenAI secret
    secret2 = cache.get_secret_string(appName + "-" + envDeploy + "_secret1")
    openaiToken = json.loads(secret2)["secret_openai"]

    # UsersFirewall secret
    secret3 = cache.get_secret_string(appName + "-" + envDeploy + "_secret1")
    idUsersAllowed = eval(json.loads(secret3)["secret_users"])

    # AdminFirewall secret
    secret4 = cache.get_secret_string(appName + "-" + envDeploy + "_secret1")
    idAdminAllowed = eval(json.loads(secret4)["secret_admins"])

    # Db key secret
    secret5 = cache.get_secret_string(appName + "-" + envDeploy + "_secret3")
    idAdminAllowed = json.loads(secret5)["secret_db"]

    # File key secret
    secret6 = cache.get_secret_string(appName + "-" + envDeploy + "_secret6")
    idAdminAllowed = json.loads(secret6)["secret_file"]


