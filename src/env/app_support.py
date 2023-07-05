# AWS libraries
import botocore 
import botocore.session 
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig 

# Python libraries
import os
import json
from dotenv import load_dotenv

# Custom importation
import src.env.app_public_env as penv

# General variables from public env
dbPath = penv.dbPath
logsPath = penv.logsPath
maxTokensPerUser = penv.maxTokensPerUser
appVersion = penv.version
maxTokensIdentity = penv.maxTokensIdentity
maxTokensResponse = penv.maxTokensResponse

# Global internal variables
settings = {
    "Identity" : 
        "You play jepetobot and you just have to respond as if you were that character. You are a member of a chat that talks about many topics and you can have opinions on those topics. Your purpose in that chat is to answer the questions in the most human way possible. Your answers are kind",

    "Temperature": 
        0.6
}


# Local secrets. Only run in your local.
if penv.execLocal:
    print("Using local env variables...")
    load_dotenv("src/env/.app.env")

    # Telegram variables
    idUsersAllowed = eval(os.environ["secret_users"])
    idAdminAllowed= eval(os.environ["secret_admins"])

    # Token variables
    telegramToken = os.environ["secret_telegram"]
    openaiToken = os.environ["secret_openai"]

    #Custom variables
    envDeploy = os.environ["ENVIRONMENT_DEPLOY"]
    awsRegion = os.environ["AWS_REGION"]

elif not penv.execLocal:
    print("Using secretmanager...")

    # Custom variables
    envDeploy = os.environ["ENVIRONMENT_DEPLOY"]
    awsRegion = os.environ["AWS_REGION"]

    # SecretManager connection
    session = botocore.session.Session()
    client = session.create_client('secretsmanager', region_name=awsRegion)
    cacheConfig = SecretCacheConfig()
    cache = SecretCache(config = cacheConfig, client = client)

    # Telegram variables
    secret1 = cache.get_secret_string(penv.appName + "-" + envDeploy + "_secret1")
    telegramToken = json.loads(secret1)["secret_telegram"]

    # OpenAI variables
    secret2 = cache.get_secret_string(penv.appName + "-" + envDeploy + "_secret1")
    openaiToken = json.loads(secret1)["secret_openai"]

    # UsersFirewall variables
    secret3 = cache.get_secret_string(penv.appName + "-" + envDeploy + "_secret1")
    idUsersAllowed = eval(json.loads(secret1)["secret_users"])

    # AdminFirewall variables
    secret3 = cache.get_secret_string(penv.appName + "-" + envDeploy + "_secret1")
    idAdminAllowed = eval(json.loads(secret1)["secret_admins"])
