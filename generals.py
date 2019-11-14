from enum import Enum

class PlayerEnum(Enum):
    Human = 1
    MinMax = 2
    QLearningPlayer = 3
    Random = 4
    SVMPlayer = 5

class State(Enum):
    EMPTY = 0
    X = 1
    O = 2
    
def getInput(messageForUser):
    inp = ''
    while not inp.isdigit():
        print(messageForUser, end='')
        inp = input()
        if inp.isdigit():
            return int(inp)