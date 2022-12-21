# AWS libraries
import botocore 
import botocore.session 
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig 

# Python libraries
import os
from dotenv import load_dotenv

# Custom importation
import src.modules.app_public_env as penv

# Local secrets. Only run in your local.
if penv.execLocal:
    print("Using local env variables...")
    load_dotenv("src/modules/.env")

    # Telegram variables
    telegramToken = os.environ["TELEGRAM_TOKEN"]

elif not penv.execLocal:
    print("Using secretmanager...")
    
    # SecretManager connection
    client = botocore.session.get_session().create_client('secretsmanager')
    cache_config = SecretCacheConfig()
    cache = SecretCache( config = cache_config, client = client)

    # Telegram variables
    telegramToken = cache.get_secret_string(penv.appName + "_secret1")


