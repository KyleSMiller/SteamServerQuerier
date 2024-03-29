from ServerQuerier import ServerQuerier
from ServerQuerierA2S import ServerQuerierA2S

import json
from threading import Timer
import time

class QueryManager:
    """
    Query a set of steam servers on a set interval
    Steam servers are constructed from a .json file
    """
    def __init__(self, serverConstructorFile, outputFile=None):
        self.__serverConstructorFile = serverConstructorFile
        self.__outputFile = outputFile
        self.__serverData = {}
        self.__queryInterval = 120

    def setQueryInterval(self, queryInterval):
        self.__queryInterval = queryInterval

    def setServerConstructorFile(self, file):
        self.__serverConstructorFile = file

    def setOutputFile(self, file):
        self.__outputFile = file

    def getServerData(self):
        return self.__serverData

    def start(self, queryInterval=120, writeToJson=True):
        """
        begin the timer to query a series of steam servers
        :param writeToJson:  boolean to specify if the gathered data should be written to a .json file
        """
        self.__queryInterval = queryInterval
        time.sleep(self.__queryInterval)
        self.queryServers(writeToJson, repeat=True)
        # Timer(queryInterval, self.queryServers, [writeToJson, True]).start()
        # # TODO: add stop() functionality

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
        serverGroups = self.__parseServerConstructors()
        self.__serverData = {}  # clear the file before adding new data
        for serverGroupName, serverList in serverGroups.items():
            for server in serverList:
                server.query()
                if serverGroupName not in self.__serverData.keys():  # create a list for the server group if it does not exist
                    self.__serverData[serverGroupName] = []
                self.__serverData[serverGroupName].append(server.getAll())
        if writeToJson:
            self.writeToJson(self.__outputFile)
        print("\n--------Finished querying all servers--------\n")
        if repeat:
            self.start(queryInterval=self.__queryInterval, writeToJson=writeToJson)  # make the timer run periodically


    def __parseServerConstructors(self):
        """
        Parse the .json server constructors and create ServerQuery objects from them
        :return:  a list of created ServerQuery objects
        """
        serverGroups = {}
        with open(self.__serverConstructorFile) as jsonFile:
            data = json.load(jsonFile)
            for serverGroup, servers in data.items():
                serverGroups[serverGroup] = []  # add the server groups
                for server in servers:
                    serverGroups[serverGroup].append(ServerQuerierA2S(server["IP"], server["Query Port"],
                                                                   name=server["Name"], game=server["Game"],
                                                                   nameOverride=server["NameOverride"], gameOverride=server["GameOverride"]))
                jsonFile.close()
            return serverGroups
