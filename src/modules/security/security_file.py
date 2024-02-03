#Python libraries
from cryptography.fernet import Fernet


# Function to encrypt a file
def EncryptFile(originalFilePath, key):
    cipherSuite = Fernet(key)
    with open(originalFilePath, 'rb') as file:
        plainText = file.read()

    encryptedFileData = cipherSuite.encrypt(plainText)

    with open(originalFilePath, 'wb') as encryptedFile:
        encryptedFile.write(encryptedFileData)


# Function to decrypt a file
def DecryptFile(encryptedFilePath, key):
    cipherSuite = Fernet(key)
    
    with open(encryptedFilePath, 'rb') as file:
        encryptedFileData = file.read()

    decryptedFileData = cipherSuite.decrypt(encryptedFileData)

    with open(encryptedFilePath, 'wb') as decryptedFile:
        decryptedFile.write(decryptedFileData)