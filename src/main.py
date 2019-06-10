from ServerQuerier import ServerQuerier

import json
import time

def writeToJson(serverDataDict):
    with open("ServerQueryData.json", "w") as outfile:
       print(serverDataDict)
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
            servers.append(ServerQuerier(server["IP"], server["Query Port"]))
    # query all servers in the server list and add the data that is gathered to a dictionary
    for server in servers:
        server.query()
        serverDataDict["Server Data"].append(server.getAll())
    # save the collected data to a .json file
    writeToJson(serverDataDict)

def test():
    print("yo")


def main():
    startTime = time.time()
    # 2 minute timer
    while True:
        time.sleep(10)
        queryServers()


# queryServers()
main()