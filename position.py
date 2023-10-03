class Square:
    """each square has 3 states: empty, white, black."""
    x: int = None
    y: int = None
    EMPTY = 0
    WHITE = 1
    BLACK = 2
    
    def __init__(self, x=x, y=y, state=EMPTY):
        self.x = x
        self.y = y
        self.state = state
        
    def __repr__(self):
        return str(self.state)
    
    def __eq__(self, other):
        return self.state == other.state
    
    def __hash__(self):
        return hash(self.state)
    
    def flip(self):
        if self.state == Square.WHITE:
            self.state = Square.BLACK
        elif self.state == Square.BLACK:
            self.state = Square.WHITE
    

# shorthands
WHITE = Square.WHITE
BLACK = Square.BLACK
EMPTY = Square.EMPTY

class Position:
    """Efficient 9x9 board representation. """
    board = None
    move_stack = []
    turn = WHITE
    def __init__(self, board=None):
        if board is None:
            self.board = [[Square() for _ in range(9)] for _ in range(9)]
        else:
            self.board = board
        self.move_stack = []
    
    def check_ttt_won(self, board):
        """board is 3x3; check if won and color of winner."""
        for i in range(3):
            if board[i][0] != EMPTY and board[i][0] == board[i][1] == board[i][2]:
                return True, board[i][0]
            if board[0][i] != EMPTY and board[0][i] == board[1][i] == board[2][i]:
                return True, board[0][i]
        if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
            return True, board[0][0]
        if board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
            return True, board[0][2]
        return False, None
    
    def in_sector(self, sq: Square):
        """Check what sector the square is in. """
        return sq.x // 3, sq.y // 3
    
    def is_sector_equal(self, x, y):
        return x.x == y.x and x.y == y.y
    
    def sector_to_global(self, x, y, a, b):
        """Convert sector coordinates to global coordinates.
        x, y -> sector coordinates, a, b -> local coordinates"""
        return x * 3 + a, y * 3 + b
    
    def get_sector_squares(self, x, y):
        TOP_LEFT_x = 3 * x; TOP_LEFT_y = 3 * y
        BOTTOM_RIGHT_x = 3 * x + 2; BOTTOM_RIGHT_y = 3 * y + 2
        board = [[self.board[i][j] for j in range(TOP_LEFT_y, BOTTOM_RIGHT_y + 1)]
                 for i in range(TOP_LEFT_x, BOTTOM_RIGHT_x + 1)]
        return board
    
    def check_sector_playable(self, x, y):
        """check if the sector is still playable
        a sector is a 3x3 square.
        x: 0-2, y: 0-2
        """
        board = self.get_sector_squares(x, y)
        if self.check_ttt_won(board)[0]:
            return False
        for i in board:
            for j in i:
                if j == EMPTY:
                    return True
        return False
    
    
    def last_move(self):
        """Return the last move. """
        if len(self.move_stack) == 0:
            return None
        return self.move_stack[-1]
    
    def make_move(self, move):
        """Make a move. """
        self.move_stack.append(move)
        self.board[move.x][move.y] = move.state
        self.turn = BLACK if self.turn == WHITE else WHITE
    

class MoveGen:
    """Generate all possible moves for a given position. """
    pos = Position()
    def __init__(self, position=Position()):
        self.pos = position
        
    def all_moves(self):
        """Generate all possible moves for a given position. """
        pos = self.pos
        turn = pos.turn
        last_move = pos.last_move()
        if last_move is None:
            return [Square(i, j, WHITE) for i in range(9) for j in range(9)]
        ALL_SQUARES_OK = False
        sector = pos.in_sector(last_move)
        if not pos.check_sector_playable(sector[0], sector[1]):
            ALL_SQUARES_OK = True
        moves = []
        if ALL_SQUARES_OK:
            for i in range(9):
                for j in range(9):
                    if pos.board[i][j] == EMPTY:
                            moves.append(Square(i, j, turn))
        else:
            # Only this sector is playable
            board = pos.get_sector_squares(sector[0], sector[1])
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        x, y = pos.sector_to_global(sector[0], sector[1], i, j)
                        moves.append(Square(x, y, turn))
        return moves
            