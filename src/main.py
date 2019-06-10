from ServerQuerier import ServerQuerier

import json
import time
import threading


def writeToJson(serverDataDict):
    with open("resources\\ServerQueryData.json") as outfile:
        json.dump(serverDataDict, outfile)


def queryServers():
    """
    Query all servers provided in the .json constructor file
    Write data that is gathered to a single dictionary
    """
    servers = []
    serverDataDict = {
        "Server Data": []
    }

    # load server constructors and add them into the server list
    with open("C:\\Users\\raysp\\Desktop\\Python\\Personal\\BirbBot\\resources\\ServerConstructorInfo.json") as jsonFile:
        data = json.load(jsonFile)
        for server in data["Server Constructors"]:
            servers.append(ServerQuerier(server["Address"], server["Query Port"]))
    # query all servers in the server list and add the data that is gathered to a dictionary
    for server in servers:
        server.query()
        serverDataDict["Server Data"].append(server.getAll())
    # save the collected data to a .json file
    writeToJson(serverDataDict)


def main():
    startTime = time.time()
    # 2 minute timer
    while True:
        timer = threading.Timer(120.0, queryServers)

        # currentTime = time.time()
        # if currentTime == startTime + 120:
        #     startTime = currentTime
        #     queryServers()


queryServers()
main()