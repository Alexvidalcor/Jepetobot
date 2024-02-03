#Python libraries
from cryptography.fernet import Fernet

# Custom importation
from src.modules.security import security_crypto


# Decorator to encrypt DB params
def EncryptParams(func):
    def wrapper(*args, **kwargs):
        cipherSuite = Fernet(security_crypto.fernetDbKey)
        encrypted_args = tuple(cipherSuite.encrypt(arg.encode()).decode() if isinstance(arg, str) else arg for arg in args)
        return func(*encrypted_args, **kwargs)
    
    return wrapper


# Decorator to decrypt DB params
def DecryptParams(func):
    def wrapper(*args, **kwargs):
        cipherSuite = Fernet(security_crypto.fernetDbKey)
        decrypted_args = tuple(cipherSuite.decrypt(arg.encode()).decode() if isinstance(arg, str) else arg for arg in args)
        return func(*decrypted_args, **kwargs)
    
    return wrapper


# Function to decrypt a DB list
def DecryptList(encryptedList):

    decryptedList = []
    for encryptedElement in encryptedList:
        if  isinstance(encryptedElement, str) and len(encryptedElement) > 20:
            cipherSuite = Fernet(security_crypto.fernetDbKey)
            # Decrypt each element
            decryptedElement = cipherSuite.decrypt(encryptedElement)
            # Add the decrypted element to the new list
            decryptedList.append(decryptedElement.decode('utf-8'))  # decode from bytes to string
        else:
            decryptedList.append(encryptedElement)

    return decryptedList