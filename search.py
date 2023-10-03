"""Alpha/Beta search"""
import evaluate, tt
from position import *

best_move = None  # root move
nodes = 0
ttTable = tt.TranspositionTable(size=100000)

VALUE_WIN = 10000
def search(pos: Position, depth, alpha, beta, PvNode, rootNode=False):
    global ttTable
    global nodes
    global best_move
    nodes += 1
    
    if depth <= 0:
        return evaluate.evaluate(pos)
    
    # check for game over
    game_over, winner = pos.is_game_over()
    if game_over:
        if winner == WHITE:
            return VALUE_WIN
        elif winner == BLACK:
            return -VALUE_WIN
        else:
            return 0
    
    # TT lookup
    ttEntry = ttTable.get(pos)
    ttHit = not ttEntry.is_none()
    ttMove = ttEntry.move if ttHit else None
    ttValue = ttEntry.value if ttHit else None
    ttPv = PvNode or (ttHit and ttEntry.is_pv)
    ttEval = ttEntry.eval if ttHit else None
    
    if ttHit:
        eval_ = ttEval
        if eval_ is None:
            eval_ = evaluate.evaluate(pos)
        # We should use ttValue if it exists
        if ttValue is not None:
            eval_ = ttValue
    else:
        eval_ = evaluate.evaluate(pos)
        # Save the static eval to the TT
        ttTable.save(pos, ttTable.TTEntry(pos.__hash__(), None, None, eval_, None, None))
    
    LEGAL_MOVES = MoveGen(pos).legal_moves()
    bestValue = -100000
    for m in LEGAL_MOVES:
        value = -100000
        pos.make_move(m)
        r = 0
        newDepth = depth - 1
        if PvNode: r -= 1
        else: r += 1 if depth < 9 else 0
        if m == ttMove: r -= 1
        d = newDepth - r
        
        if PvNode:
            value = -search(pos, -(alpha+1), -alpha, d, True)
            if alpha < value < beta:
                value = -search(pos, -beta, -alpha, d, False)
        else:
            value = -search(pos, -beta, -alpha, d, False)
            
        # Do full depth search when reduced LMR search fails high
        if value > alpha and d < depth - 1:
            doDeeperSearch = value > bestValue + 45
            doEvenDeeperSearch = value > alpha + 200
            doShallowerSearch = value < bestValue + newDepth
            newDepth += doDeeperSearch + doEvenDeeperSearch - doShallowerSearch
            
            if newDepth > d:
                value = -search(pos,-(alpha+1), -alpha, newDepth, False)
        pos.undo_move()
    
        if value > bestValue:
            bestValue = value
            if value > alpha:
                if rootNode:
                    best_move = m  # no need to update best_move if not root node
                if value >= beta:
                    break
                else:
                    alpha = value
    
    # Save to TT
    ttTable.save(pos, ttTable.TTEntry(pos.__hash__(), best_move, bestValue, eval_, depth, PvNode))
    return bestValue


def iterative_deepening(pos: Position, depth=10):
    global nodes
    global best_move
    nodes = 0
    best_move = None
    for d in range(1, depth+1):
        bestValue = search(pos, d, -100000, 100000, True, True)
        print(f"info depth {d} nodes {nodes} score cp {bestValue} pv {best_move}")
    
    return best_move