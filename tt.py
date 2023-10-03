"""Acknowledgements to PyFish for basic tt code."""

from position import *

class TranspositionTable:
    class TTEntry:
        def __init__(self, key=None, move: Square = None, value: int = None, eval: int = None,
                     depth: int = None, is_pv: bool = None):
            self.key = key
            self.move = move
            self.value = value
            self.eval = eval
            self.depth = depth
            self.is_pv = is_pv
        
        def is_none(self):
            return self.key is None
    
    def __init__(self, size: int):
        self.size = size
        # self.table = [self.TTEntry() for i in range(self.size)]
        self.table = dict()
    
    def hashfull_count(self):
        return sum([1 for entry in self.table if not entry.is_none()])
    
    def hashfull(self):
        return self.hashfull_count() / self.size
    
    def hash(self, pos: Position):
        return pos.__hash__() % self.size
    
    def get(self, pos: Position):
        return self.table[pos] if pos in self.table else self.TTEntry()
    
    def save(self, pos, entry: TTEntry):
        self.table[pos] = entry
    
    def clear(self):
        # self.table = [self.TTEntry() for i in range(self.size)]
        self.table = dict()
    
    def __str__(self):
        return str(self.table)

