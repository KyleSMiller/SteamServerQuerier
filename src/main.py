"""
Run the server querier
"""
from QueryManager import QueryManager
import time


# serverQuerier.start(queryInterval=60, writeToJson=True)
while True:
    serverQuerier = QueryManager(
        "C:\\Users\\raysp\\Desktop\\Python\\Personal\\SteamServerQuerier\\src\\ServerConstructorInfo.json",
        "C:\\Users\\raysp\\Desktop\\Python\\Personal\\SteamServerQuerier\\src\\ServerQueryData.json",
    )
    serverQuerier.queryServers(writeToJson=True, repeat=False)
    serverQuerier = None
    time.sleep(60)
