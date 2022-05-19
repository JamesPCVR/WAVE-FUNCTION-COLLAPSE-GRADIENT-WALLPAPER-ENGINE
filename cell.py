import random
from tile import Tile

class Cell:
    def __init__(self, superposition:list):
        self.__superposition = superposition
        self.__state = Tile("tiles/unknown.png", [-1, -1, -1, -1])
        self.calculateEntropy()

    def calculateEntropy(self):
        if len(self.__superposition) == 1:
            self.__entropy = 0
            return
        entropy = 0
        for tile in self.__superposition:
            entropy += tile.getEntropyWeight()
        self.__entropy = entropy

    def getEntropy(self):
        return self.__entropy
    
    def setState(self):
        self.__state = self.__superposition[0]
        self.calculateEntropy()
    
    def setRandomState(self):
        weighttotal = 0
        for tile in self.__superposition:
            weighttotal += tile.getRandomWeight()
        randnum = random.randint(0, weighttotal - 1)
        for tile in self.__superposition:
            randnum -= tile.getRandomWeight()
            if randnum <= 0:
                self.__superposition = [tile]
                break
        self.setState()
    
    def getState(self):
        return self.__state

    def removeSuperposition(self, connector:int, connectorindex:int, board:list, position:tuple):
        if self.getEntropy() == 0:
            return
        temp = []
        for tile in self.__superposition:
            adjacency = tile.getAdjacency()
            if adjacency[connectorindex] == connector:
                temp.append(tile)
        self.__superposition = temp
        self.calculateEntropy()
        if self.getEntropy() == 0:
            self.setState()
            self.propagateChange(board, position)
    
    def propagateChange(self, board, position):
        up = (position[0] - 1, position[1])
        right = (position[0], position[1] + 1)
        down = (position[0] + 1, position[1])
        left = (position[0], position[1] - 1)

        if up[0] != -1:
            board[up[0]][up[1]].removeSuperposition(self.__state.getAdjacency()[0], 2, board, up)
        
        if right[1] != len(board[0]):
            board[right[0]][right[1]].removeSuperposition(self.__state.getAdjacency()[1], 3, board, right)
        
        if down[0] != len(board):
            board[down[0]][down[1]].removeSuperposition(self.__state.getAdjacency()[2], 0, board, down)
        
        if left[1] != -1:
            board[left[0]][left[1]].removeSuperposition(self.__state.getAdjacency()[3], 1, board, left)
