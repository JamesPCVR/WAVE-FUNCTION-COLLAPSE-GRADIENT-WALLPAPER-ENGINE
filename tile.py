class Tile:
    def __init__(self, imagepath:str, adjacency:list, randomweight:int=1, entropyweight:int=1):
        self.__imagepath = imagepath
        self.__adjacency = adjacency
        self.__entropyweight = entropyweight
        self.__randomweight = randomweight
    
    def getImagePath(self):
        return self.__imagepath
    
    def getEntropyWeight(self):
        return self.__entropyweight
    
    def getAdjacency(self):
        return self.__adjacency
    
    def getRandomWeight(self):
        return self.__randomweight