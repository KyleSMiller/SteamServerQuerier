"""
Run the server querier
"""
from QueryManager import MultiQuerier

serverQuerier = MultiQuerier(
                             "C:\\Users\\raysp\\Desktop\\Python\\Personal\\BirbBot\\resources\\ServerConstructorInfo.json",
                             "C:\\Users\\raysp\\Desktop\\Python\\Personal\\SteamServerQuerier\\src\\ServerQueryData.json",
                             )

serverQuerier.queryServers()
serverQuerier.start(queryInterval=20.0, writeToJson=True)