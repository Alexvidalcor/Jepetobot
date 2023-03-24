# Custom modules
from main import *
from src.permissions import UsersFirewall
from src.db import OperateStatsToken


def StatsNumTokens(username, queryResults):

    numTokens = sum([len(list(element["content"]))
                    for element in queryResults])

    if len(queryResults) <= 2:
        OperateStatsToken(username, numTokens, option="insert")
    else:
        historicTokens = OperateStatsToken(username, numTokens)
        OperateStatsToken(username, historicTokens+numTokens, option="update")


