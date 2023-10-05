import search, search_mcts
from position import *

MAX_DEPTH = 256
MAX_TIME = 10**9

MCTS_ENABLED = False

def uti():
    command = input()
    command = command.strip()
    pos = Position()
    depth = MAX_DEPTH
    movetime = MAX_TIME

    if command.startswith("go"):
        if command.split(" ").__len__() > 1 and command.split(" ")[1] == "movetimr":
            movetime = int(command.split(" ")[2])
        
        if command.split(" ").__len__() > 1 and command.split(" ")[1] == "infinite":
            movetime = MAX_TIME

        if MCTS_ENABLED:
            search_mcts.search(pos)
        else:
            search.iterative_deepening(pos, depth)