# AWS libraries
import botocore 
import botocore.session 
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig 

# Python libraries
import os
import json
from dotenv import load_dotenv


# Variables from GithubSecrets/environment
try:
    print("Using local env secrets...")
    load_dotenv("src/env/.app.env")

    # Telegram variables
    idUsersAllowed = eval(os.environ["APP_USERSALLOWED"])
    idAdminAllowed= eval(os.environ["APP_ADMINSALLOWED"])

    # Token variables
    telegramToken = os.environ["TELEGRAM_TOKEN"]
    openaiToken = os.environ["OPENAI_TOKEN"]

    #Custom variables
    envDeploy = os.environ["ENVIRONMENT_DEPLOY"]
    awsRegion = os.environ["AWS_REGION"]
    dbKey = os.environ["DB_KEY"]
    fileKey = os.environ["FILE_KEY"]
    appName = os.environ["APP_NAME"]

except KeyError:
    print("Failed!\nUsing secretmanager...")

    # Custom variables
    envDeploy = os.environ["ENVIRONMENT_DEPLOY"]
    awsRegion = os.environ["AWS_REGION"]
    appName = os.environ["APP_NAME"]

    # SecretManager connection
    session = botocore.session.Session()
    client = session.create_client('secretsmanager', region_name=awsRegion)
    cacheConfig = SecretCacheConfig()
    cache = SecretCache(config = cacheConfig, client = client)

    # Telegram secret
    secret1 = cache.get_secret_string(appName + "-" + envDeploy + "_Secretmanager-secret1")
    telegramToken = json.loads(secret1)["secret_telegram"]

    # OpenAI secret
    openaiToken = json.loads(secret1)["secret_openai"]

    # UsersFirewall secret
    idUsersAllowed = eval(json.loads(secret1)["secret_users"])

    # AdminFirewall secret
    idAdminAllowed = eval(json.loads(secret1)["secret_admins"])

    # Db key secret
    secret3 = cache.get_secret_string(appName + "-" + envDeploy + "_Secretmanager-secret3")
    dbKey = json.loads(secret3)["secret_db"]

    # File key secret
    secret4 = cache.get_secret_string(appName + "-" + envDeploy + "_Secretmanager-secret4")
    fileKey = json.loads(secret4)["secret_file"]


