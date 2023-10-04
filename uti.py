import search_mcts
from position import *

MAX_DEPTH = 256
MAX_TIME = 10**9
def uti():
    command = input()
    command = command.strip()
    pos = Position()
    if command.startswith("go"):
        if command.split(" ").__len__() > 1 and command.split(" ")[1] == "movetimr":
            movetime = int(command.split(" ")[2])
        else:
            movetime = MAX_TIME
        
        if command.split(" ").__len__() > 1 and command.split(" ")[1] == "infinite":
            movetime = MAX_TIME

        # search.iterative_deepening(pos, depth)
        search_mcts.search(pos)
