from ServerQuerier import ServerQuerier

import json
from threading import Timer

class QueryManager:
    """
    Query a set of steam servers on a set interval
    Steam servers are constructed from a .json file
    """
    def __init__(self, serverConstructorFile, outputFile=None):
        self.__serverConstructorFile = serverConstructorFile
        self.__outputFile = outputFile
        self.__serverData = {"Server Data": []}

    def setQueryInterval(self, queryInterval):
        self.__queryInterval = queryInterval

    def setServerConstructorFile(self, file):
        self.__serverConstructorFile = file

    def setOutputFile(self, file):
        self.__outputFile = file

    def getServerData(self):
        return self.__serverData

    def start(self, queryInterval=120.0, writeToJson=True):
        """
        begin the timer to query a series of steam servers
        :param writeToJson:  boolean to specify if the gathered data should be written to a .json file
        """
        Timer(queryInterval, self.queryServers, [writeToJson, True]).start()
        # TODO: add stop() functionality

    def writeToJson(self, outputFile):
        with open(outputFile, "w") as outfile:
            json.dump(self.__serverData, outfile)
            outfile.close()

    def queryServers(self, writeToJson=True, repeat=False):
        """
        Query all servers provided in the .json constructor file
        Write data that is gathered to a single dictionary
        :param writeToJson:  boolean to specify if the gathered data should be written to a .json file
        :param repeat:  boolean for if the process should operate in a periodic timer. True will call start()
        """
        servers = self.__parseServerConstructors()
        self.__serverData["Server Data"] = []  # clear the file before adding new data
        for server in servers:
            server.query()
            self.__serverData["Server Data"].append(server.getAll())
        if writeToJson:
            self.writeToJson(self.__outputFile)
        if repeat:
            self.start(writeToJson)  # make the timer run periodically


    def __parseServerConstructors(self):
        """
        Parse the .json server constructors and create ServerQuery objects from them
        :return:  a list of created ServerQuery objects
        """
        servers = []
        with open(self.__serverConstructorFile) as jsonFile:
            data = json.load(jsonFile)
            for server in data["Server Constructors"]:
                servers.append(ServerQuerier(server["IP"], server["Query Port"], server["Name"], game=server["Game"]))
            jsonFile.close()
        return servers