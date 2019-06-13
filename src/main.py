"""
Run the server querier
"""
from QueryManager import QueryManager

serverQuerier = QueryManager(
                             "C:\\Users\\raysp\\Desktop\\Python\\Personal\\BirbBot\\resources\\ServerConstructorInfo.json",
                             "C:\\Users\\raysp\\Desktop\\Python\\Personal\\SteamServerQuerier\\src\\ServerQueryData.json",
                             )

serverQuerier.queryServers()
serverQuerier.start(queryInterval=120.0, writeToJson=True)