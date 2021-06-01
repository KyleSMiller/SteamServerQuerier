import valve.source.a2s
import valve.source.messages


class ServerQuerier:
    """
    Query a Steam Server and store the response in a dictionary
    """
    def __init__(self, serverIP, queryPort, name="Unknown Steam Server", game="Unknown Game",
                 nameOverride=False, gameOverride=False):
        self.__serverIP = (serverIP.split(":")[0] if ":" in serverIP else serverIP)
        self.__port = (serverIP.split(":")[1] if ":" in serverIP else None)
        self.__queryPort = int(queryPort)
        self.__name = name
        self.__game = game
        self.__nameOverride = True if nameOverride == "True" else False
        self.__gameOverride = True if gameOverride == "True" else False
        self.__gameType = ""  # by default, do not display GameType
        self.__map = "Unknown Map"
        self.__currentPlayers = "?"
        self.__maxPlayers = "?"
        self.__playerList = []

        self.__dataDict = {}


    def getName(self):
        return self.__name

    def getGame(self):
        return self.__game

    def getGameType(self):
        return self.__gameType

    def getMap(self):
        return self.__map

    def getCurrentPlayers(self):
        return self.__currentPlayers

    def getMaxPlayers(self):
        return self.__maxPlayers

    def getPlayerList(self):
        return self.__playerList

    def getPopulation(self):
        """
        return a formatted string of server population
        :return: currentPlayers/maxPlayers
        """
        return str(self.__currentPlayers) + "/" + str(self.__maxPlayers)

    def getAll(self):
        """
        Get the dictionary of all collected server data
        :return: a dictionary of server data
        """
        return self.__dataDict

    def query(self):
        """
        Query the steam server
        """
        self.__playerList = []  # clear the playerList
        serverAddress = (self.__serverIP, self.__queryPort)
        try:
            with valve.source.a2s.ServerQuerier(serverAddress) as server:
                info = server.info()
                if self.__nameOverride == False:
                    self.__name = "{server_name}".format(**info)
                if self.__gameOverride == False:
                    self.__game = "{game}".format(**info)
                self.__gameType = self.__decodeGameType("{server_tags}".format(**info))
                self.__map = "{map}".format(**info)
                self.__currentPlayers = "{player_count}".format(**info)
                self.__maxPlayers = "{max_players}".format(**info)
                for player in server.players()["players"]:
                    self.__playerList.append("{name}".format(**player))
            self.__writeToDictionary()

        except valve.source.messages.BrokenMessageError as err:
            print(err)
            if self.__port is not None:
                print("Server " + str(self.__serverIP) + ":" + str(self.__port) + " exists, but "
                      + str(self.__queryPort) + " is not the correct query port.")
            else:
                print("Server " + str(self.__serverIP) + " exists, but "
                      + str(self.__queryPort) + " is not the correct query port.")
            # give the data dict for the server the minimum amount of data needed to create a ServerInfo object
            self.__dataDict["Status"] = "Offline"
            self.__dataDict["Name"] = self.getName()
            self.__dataDict["Game"] = self.getGame()

        except valve.source.NoResponseError as err:
            print(err)
            if self.__port is not None:
                print("Server " + str(self.__serverIP) + ":" + str(self.__port) +
                      " is either offline, is not a steam server, or does not exist")
            else:
                print("Server " + str(self.__serverIP) + " is either offline, is not a steam server, or does not exist")
            # give the data dict for the server the minimum amount of data needed to create a ServerInfo object
            self.__dataDict["Status"] = "Offline"
            self.__dataDict["Name"] = self.getName()
            self.__dataDict["Game"] = self.getGame()



    def __writeToDictionary(self):
        """
        Write all gathered data to a dictionary that can be converted into a .json file
        """
        self.__dataDict["IP"] = (str(self.__serverIP) + ":" + str(self.__port) if self.__port != None else self.__serverIP)
        self.__dataDict["Query Port"] = self.__queryPort
        self.__dataDict["Status"] = "Online"
        self.__dataDict["Name"] = self.getName()
        self.__dataDict["Game"] = self.getGame()
        self.__dataDict["Game Type"] = self.getGameType()
        self.__dataDict["Map"] = self.getMap()
        self.__dataDict["Population"] = self.getPopulation()
        self.__dataDict["Player List"] = self.getPlayerList()
        print(self.__dataDict)

    def __decodeGameType(self, encodedGameType):
        """
        python-valve does not correctly decode the returned GameType, so do it manually here
        Example of encoded GameType:  "bTq1@H:500710000,C:523,B:0,N:Frontline,M:15001"
        :param encodedGameType:  the encoded GameType string returned by server_tags
        :return:  the decoded GameType
        """
        if "N:" not in encodedGameType:
            return ""  # return no GameType rather than "Unknown Game Type". This is just a preference thing
        else:
            for field in encodedGameType.split(","):
                if "N:" in field:
                    return field.split(":")[1] + " "  # just add an extra space to the end because I'm lazy
            return ""


# test = ServerQuerier("66.151.138.224:3175", 3177)
# test.query()

# TypeError: <valve.source.messages.PlayerEntry object at 0x0000026336EA4828> is not JSON serializable
