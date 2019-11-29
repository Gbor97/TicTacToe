from enum import Enum
import pickle

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

def save(name, thing):
    fw = open(name, 'wb')
    pickle.dump(thing, fw)
    fw.close()

def load(file):
    fr = open(file, 'rb')
    thing = pickle.load(fr)
    fr.close()
    return thing

def transfromBoardState5(boardStateHash):
    result = []
    for i in range(len(boardStateHash)):
        if boardStateHash[i] == '1':
            result.append(1)
            result.append(0)
        elif boardStateHash[i] == '2':
            result.append(0)
            result.append(1)
        else:
            result.append(0)
            result.append(0)
    return result

# get unique hash of current board state
def getHash(boardState):
    boardHash = ""
    for k in range(len(boardState)):
        for l in range(len(boardState)):
            boardHash += str(boardState[k][l].state.value)
    return boardHash

def getRivalSign(sign):
    if sign == State.X:
        return State.O
    else:
        return State.X