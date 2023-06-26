# Python libraries
import logging
from logging.handlers import RotatingFileHandler
import datetime
import sys

# Modules imported
from src.modules.app_support import logsPath


# Global exceptions handler
def ExceptionHandler(type, value, traceback):
    # Registrar la excepción utilizando logging
    errorsLogger.critical("Error found: ", exc_info=(type, value, traceback))
sys.excepthook = ExceptionHandler


#Formatter config
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


# Application log
appLogger = logging.getLogger('app_logger')
appLogger.setLevel(logging.INFO)

appHandler = RotatingFileHandler(f'{logsPath}/app.log', maxBytes=5000000, backupCount=5)
appHandler.setFormatter(formatter)

appLogger.addHandler(appHandler)
appLogger.info('------------Init app logs')


# User interaction log
userLogger = logging.getLogger('user_logger')
userLogger.setLevel(logging.DEBUG)

userHandler = RotatingFileHandler(f'{logsPath}/user.log', maxBytes=5000000, backupCount=5)
userHandler.setFormatter(formatter)

userLogger.addHandler(userHandler)
userLogger.info('------------Init user logs')


# Common and critical errors log
errorsLogger = logging.getLogger('errors_logger')
errorsLogger.setLevel(logging.ERROR)

errorsHandler = RotatingFileHandler(f'{logsPath}/errors.log', maxBytes=5000000, backupCount=5)
errorsHandler.setFormatter(formatter)

errorsLogger.addHandler(logging.StreamHandler())
errorsLogger.addHandler(errorsHandler)
errorsLogger.error('------------Init error logs')