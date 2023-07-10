# Custom modules
from src.modules import logtool, db
from src.env.app_public_env import maxTokensPerUser

def StatsNumTokens(username, queryResults):

    numTokens = sum([len(list(element["content"]))
                    for element in queryResults if element["content"] != "None"])

    if len(queryResults) <= 3:
        db.OperateStatsToken(username, numTokens, option="insert")
        logtool.userLogger.info('Init user logs')
    else:
        historicTokens = db.OperateStatsToken(username, numTokens)
        db.OperateStatsToken(username, historicTokens+numTokens, option="update")

    limitMaxTokens = db.OperateStatsToken(username, numTokens)
    if limitMaxTokens >= maxTokensPerUser:
        logtool.userLogger.warning(
            f"{username} exceeds MaxTokens with {limitMaxTokens }")
