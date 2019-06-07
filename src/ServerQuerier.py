import valve.source.a2s


class ServerQuerier:
    """
    Query a Steam Server and store the response in a dictionary
    """
    def __init__(self, serverIP, queryPort):
        self.__serverIP = serverIP
        self.__queryPort = queryPort

        self.__name = "Unknown Steam Server"
        self.__game = "Unknown Game"
        self.__map = "Unknown Map"
        self.__currentPlayers = "?"
        self.__maxPlayers = "?"
        self.__playerList = []


    def getName(self):
        return self.__name

    def getGame(self):
        return self.__game

    def getMap(self):
        return self.__map

    def getCurrentPlayers(self):
        return self.__currentPlayers

    def getMaxPlayers(self):
        return self.__maxPlayers

    def getPopulation(self):
        """
        return a formatted string of server population
        :return: (currentPlayers/maxPlayers)
        """
        return "(" + str(self.__currentPlayers) + "/" + str(self.__maxPlayers) + ")"

    def query(self):
        """
        Query the steam server
        """
        serverAddress = (self.__serverIP, self.__queryPort)
        with valve.source.a2s.ServerQuerier(serverAddress) as server:
            info = server.info()
            self.__name = "{server_name}".format(**info)
            self.__game = "{game}".format(**info)
            self.__map = "{map}".format(**info)
            self.__currentPlayers = "{player_count}".format(**info)
            self.__maxPlayers = "{max_players}".format(**info)
            self.__playerList = server.players()
