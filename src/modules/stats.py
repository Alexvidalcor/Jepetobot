# Import libraries
import tiktoken

# Custom modules
from src.modules import logtool, db
from src.env.app_public_env import maxTokensUserGpt, maxTokensUserDalle, maxTokensUserWhisper, maxTokensUserTts, maxTokensUserVision



#Function that calculate openai tokens
def CalculateOpenAiTokens(inputReceived, option="gpt"):
    
    if option == "gpt":
        inputReceivedJoined = "".join(inputReceived)
        encoding = tiktoken.encoding_for_model("gpt-4-1106-preview")
        countTokens = len(encoding.encode(inputReceivedJoined))

    elif option == "tts":
        inputReceivedJoined = "".join(inputReceived)
        encoding = tiktoken.encoding_for_model("gpt-4")
        countTokens = len(encoding.encode(inputReceivedJoined))
    
    return countTokens



# Function that process the number of GPT tokens
def StatsNumTokensGpt(username, userId, queryResults):

    numTokens = CalculateOpenAiTokens([element["content"] for element in queryResults if element["content"] != "None"])

    if db.OperateStatsToken(username, userId, 1, option="gptCheck") is None:
        db.OperateStatsToken(username, userId, numTokens, option="gptInsert")
    else:
        # Not first user message
        db.OperateStatsToken(username, userId, numTokens, option="gptUpdate")
        


# Function that process the number of Dalle tokens
def StatsNumTokensDalle(username, userId):

    if db.OperateStatsToken(username, userId, 1, option="dalleCheck") is None:
        db.OperateStatsToken(username, userId, 1, option="dalleInsert")
    else:
        db.OperateStatsToken(username, userId, 1, option="dalleUpdate")



# Function that process the number of Whisper tokens
def StatsNumTokensWhisper(username, userId, audioLength):

    if db.OperateStatsToken(username, userId, 1, option="whisperCheck") is None:
        db.OperateStatsToken(username, userId, audioLength, option="whisperInsert")
    else:
        db.OperateStatsToken(username, userId, audioLength, option="whisperUpdate")



# Function that process the number of tts tokens
def StatsNumTokensTts(username, userId, botAudioReply, option="tts"):

    numTokens = CalculateOpenAiTokens(botAudioReply)

    if db.OperateStatsToken(username, userId, 1, option="ttsCheck") is None:
        db.OperateStatsToken(username, userId, numTokens, option="ttsInsert")
    else:
        db.OperateStatsToken(username, userId, numTokens, option="ttsUpdate")



# Function that process the number of vision tokens
def StatsNumTokensVision(username, userId):

    if db.OperateStatsToken(username, userId, 1, option="visionCheck") is None:
        db.OperateStatsToken(username, userId, 1, option="visionInsert")
    else:
        db.OperateStatsToken(username, userId, 1, option="visionUpdate")


# Check if the user has exceeded the token limits set in the configuration
def CheckTokenLimit(username, userId):
    tokensUsed = db.OperateStatsToken(username, userId, 1, option="gptCheck")[3:8]

    if (tokensUsed[0] < maxTokensUserGpt and
    tokensUsed[1] < maxTokensUserDalle and
    tokensUsed[2] < maxTokensUserWhisper and
    tokensUsed[3] < maxTokensUserTts and
    tokensUsed[4] < maxTokensUserVision):
        result = True
    else:
        result = False

    return result
    


        



