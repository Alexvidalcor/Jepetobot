#Python libraries
import base64
from cryptography.fernet import Fernet

# Custom importation
from src.modules.security import security_crypto
from src.env.app_secrets_env import dbKey, fileKey


def GenerateFernetKey(fileKey):

    # Convert the string to bytes
    keyBytes = fileKey.encode('utf-8')

    # Encode the bytes to base64
    baseKey = base64.urlsafe_b64encode(keyBytes)

    # Ensure the key has exactly 32 bytes
    fernetKey = baseKey.ljust(32, b'=')

    return fernetKey

fernetDbKey = security_crypto.GenerateFernetKey(dbKey)
fernetFileKey = security_crypto.GenerateFernetKey(fileKey)


