# AWS libraries
import botocore 
import botocore.session 
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig 

# Python libraries
import os
import json
from dotenv import load_dotenv

# Custom importation
import src.modules.app_public_env as penv

# Local secrets. Only run in your local.
if penv.execLocal:
    print("Using local env variables...")
    load_dotenv("src/modules/.env")

    # Telegram variables
    idUsersAllowed = eval(os.environ["idUsersAllowed"])

    telegramToken = os.environ["password"]
    openaiToken = os.environ["openai_token"]

elif not penv.execLocal:
    print("Using secretmanager...")

    # SecretManager connection
    client = botocore.session.get_session().create_client('secretsmanager')
    cache_config = SecretCacheConfig()
    cache = SecretCache(config = cache_config, client = client)

    # Telegram variables
    secret1 = cache.get_secret_string(penv.appName + "_secret1")
    telegramToken = json.loads(secret1)["password"]

    # OpenAI variables
    secret2 = cache.get_secret_string(penv.appName + "_secret1")
    openaiToken = json.loads(secret1)["openai_token"]

    # UsersFirewall variables
    secret3 = cache.get_secret_string(penv.appName + "_secret1")
    idUsersAllowed: = json.loads(secret1)["idUsersAllowed"]
