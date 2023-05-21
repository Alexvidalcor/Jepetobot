# Custom modules
from main import *
from src.permissions import UsersFirewall
from src.db import OperateStatsToken


def StatsNumTokens(username, queryResults):

    numTokens = sum([len(list(element["content"]))
                    for element in queryResults if element["content"] != "None"])

    print(queryResults)
    if len(queryResults) <= 3:
        print("AL")
        OperateStatsToken(username, numTokens, option="insert")
        userLogger.info('Init user logs')
    else:
        historicTokens = OperateStatsToken(username, numTokens)
        OperateStatsToken(username, historicTokens+numTokens, option="update")

    limitMaxTokens = OperateStatsToken(username, numTokens)
    if limitMaxTokens >= maxTokensPerUser:
        userLogger.warning(
            f"{username} exceeds MaxTokens with {limitMaxTokens }")
