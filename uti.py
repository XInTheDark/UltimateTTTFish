import search
from position import *

MAX_DEPTH = 256

def uti():
    command = input()
    command = command.strip()
    pos = Position()
    if command.startswith("go"):
        if command.split(" ").__len__() > 1 and command.split(" ")[1] == "depth":
            depth = int(command.split(" ")[2])
        else:
            depth = MAX_DEPTH
        
        if command.split(" ").__len__() > 1 and command.split(" ")[1] == "infinite":
            depth = MAX_DEPTH
        
        search.iterative_deepening(pos, depth)