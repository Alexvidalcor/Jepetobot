# Import libraries
import tiktoken

# Custom modules
from src.modules import logtool, db
from src.env.app_public_env import maxTokensPerUser



#Function that calculate openai tokens
def CalculateOpenAiTokens(inputReceived):
    
    inputReceivedJoined = "".join(inputReceived)
    encoding = tiktoken.encoding_for_model("gpt-4-1106-preview")
    countTokens = len(encoding.encode(inputReceivedJoined))
    
    return countTokens



# Function that process the number of tokens
def StatsNumTokens(username, queryResults):

    numTokens = CalculateOpenAiTokens([element["content"] for element in queryResults if element["content"] != "None"])

    # First user message
    if len(queryResults) <= 3:
        db.OperateStatsToken(username, numTokens, option="insert")
        logtool.userLogger.info('Init user logs')
    else:
        # Not first user message
        historicTokens = db.OperateStatsToken(username, numTokens)
        db.OperateStatsToken(username, historicTokens+numTokens, option="update")

    # Check if user exceeds maxTokensPerUser
    limitMaxTokens = db.OperateStatsToken(username, numTokens)
    if limitMaxTokens >= maxTokensPerUser:
        logtool.userLogger.warning(
            f"{username} exceeds MaxTokens with {limitMaxTokens }")


