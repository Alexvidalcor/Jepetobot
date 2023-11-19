# Import libraries
import tiktoken

# Custom modules
from src.modules import logtool, db
from src.env.app_public_env import maxGptTokenUser



#Function that calculate openai tokens
def CalculateOpenAiTokens(inputReceived, option="gpt"):
    
    if option == "gpt":
        inputReceivedJoined = "".join(inputReceived)
        encoding = tiktoken.encoding_for_model("gpt-4-1106-preview")
        countTokens = len(encoding.encode(inputReceivedJoined))
    
    return countTokens



# Function that process the number of GPT tokens
def StatsNumTokensGpt(username, queryResults):

    numTokens = CalculateOpenAiTokens([element["content"] for element in queryResults if element["content"] != "None"])

    # First user message
    if len(queryResults) <= 3:
        db.OperateStatsToken(username, numTokens, option="gptInsert")
    else:
        # Not first user message
        historicTokens = db.OperateStatsToken(username, numTokens)
        db.OperateStatsToken(username, historicTokens+numTokens, option="gptUpdate")

    # Check if user exceeds maxGptTokenUser
    limitMaxTokens = db.OperateStatsToken(username, numTokens)
    if limitMaxTokens >= maxGptTokenUser:
        logtool.userLogger.warning(
            f"{username} exceeds MaxGptTokens with {limitMaxTokens }")
        


# Function that process the number of Dalle tokens
def StatsNumTokensDalle(username):

    if db.OperateStatsToken(username, 1, option="dalleCheck") is None:
        db.OperateStatsToken(username, 1, option="dalleInsert")
    else:
        print(db.OperateStatsToken(username, 1, option="dalleCheck"))
        db.OperateStatsToken(username, 1, option="dalleUpdate")


        



