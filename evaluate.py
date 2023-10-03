from position import *
import random

def evaluate(pos: Position):
    """Evaluation from side to move's POV."""
    us = pos.turn
    them = ~us
    
    HCESCORE = 0
    # Occupied sectors
    for i in range(3):
        for j in range(3):
            info = pos.check_sector_playable(i, j)
            if not info[0] and info[1] is not None:
                if info[1] == us:
                    HCESCORE += 50
                elif info[1] == them:
                    HCESCORE -= 50
            else:
                sector = pos.get_sector_squares(i, j)
                HCESCORE += evaluate_sector(sector)
    
    RANDOM_FACTOR = 5
    HCESCORE += random.randint(-RANDOM_FACTOR, RANDOM_FACTOR)
    
    return HCESCORE


def evaluate_sector(sector):
    """Evaluate a sector."""
    # TODO: Implement
    return 0