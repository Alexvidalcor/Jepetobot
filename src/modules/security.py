
# Custom importation
from src.env.app_secrets_env import idAdminAllowed, idUsersAllowed
from main import *

# User logging decorator
def UsersFirewall(originalFunction):
    async def CheckPermissions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message != None:
            user = update.message.from_user
            if user["id"] in idUsersAllowed:
                return await originalFunction(update, context)
            await update.message.reply_html(
                rf"Hi {user.mention_html()}!, you don't have permissions {user['id']}"
            )
        else:
            return await originalFunction(update, context) 

    return CheckPermissions


# Adminlogging decorator
def AdminFirewall(originalFunction):
    async def CheckPermissions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message != None:
            admin = update.message.from_user
            if admin["id"] in idAdminAllowed:
                return await originalFunction(update, context)
            await update.message.reply_html(
                rf"Hi {admin.mention_html()}!, you don't have admin permissions {admin['id']}"
            )
        else:
            return await originalFunction(update, context) 

    return CheckPermissions

def GenerateFernetKey():

    # Convert the string to bytes
    keyBytes = fileKey.encode('utf-8')

    # Encode the bytes to base64
    baseKey = base64.urlsafe_b64encode(keyBytes)

    # Ensure the key has exactly 32 bytes
    fernetKey = baseKey.ljust(32, b'=')

    return fernetKey


# Function to encrypt a file
def EncryptFile(originalFilePath, key):
    cipherSuite = Fernet(key)
    with open(originalFilePath, 'rb') as file:
        plainText = file.read()

    encryptedFileData = cipherSuite.encrypt(plainText)

    with open(originalFilePath, 'wb') as encryptedFile:
        encryptedFile.write(encryptedFileData)
