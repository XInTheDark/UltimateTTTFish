import search
from position import *

MAX_DEPTH = 1024
rootPos = Position()

def cmd():
    global rootPos
    command = input()
    command = command.strip()
    if command.startswith("go"):
        if command.split(" ").__len__() > 1 and command.split(" ")[1] == "depth":
            depth = int(command.split(" ")[2])
        else:
            depth = MAX_DEPTH
        
        if command.split(" ").__len__() > 1 and command.split(" ")[1] == "infinite":
            depth = MAX_DEPTH
        
        search.iterative_deepening(rootPos, depth)
        
    elif command.startswith("position fen"):
        fen = command.split(" ")[2:]
        rootPos = UTI().from_fen(" ".join(fen))
    
    elif command.startswith("move"):
        sq = (command.split(" ")[1][0], command.split(" ")[1][1])
        rootPos.make_move(Square(int(sq[0]), int(sq[1])))
        
    elif command.startswith("undomove"):
        rootPos.undo_move()

def uti():
    while True:
        cmd()