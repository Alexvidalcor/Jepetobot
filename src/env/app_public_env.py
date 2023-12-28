'''
-------------------------------------------------------
Variables that do not need to be stored as secrets and modify the behavior of the application
-------------------------------------------------------
'''

appName = "Jepetobot"
voiceChoice = "onyx" # alloy, echo, fable, onyx, nova, shimmer


'''
-------------------------------------------------------
Internal paths
-------------------------------------------------------
'''

dbName = "MainDb.sqlite"
dbPath = "src/db"
logsPath = "src/logs"


'''
-------------------------------------------------------
Token Limits
-------------------------------------------------------
'''

maxTokensUserGpt = 10000
maxTokensUserDalle = 30
maxTokensUserWhisper = 10000
maxTokensUserTts = 10000
maxTokensUserVision = 30

maxTokensCustomIdentity = 300
maxTokensBotResponseGeneral = 500


'''
-------------------------------------------------------
Others
-------------------------------------------------------
'''

configBotResponses = {
    "Identity" : 
        "You play jepetobot and you just have to respond as if you were that character. You are a member of a chat that talks about many topics and you can have opinions on those topics. Your purpose in that chat is to answer the questions in the most human way possible. Your answers are kind. You can manage images, voice and text",

    "Temperature": 
        0.6
}

appVersion = "Local" # it should be always the last line in this file (for better github actions deploy)