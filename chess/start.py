class ChessPiece:
    """Base class for all chess pieces."""
    def __init__(self, color):
        self.color = color  # 'white' or 'black'
    
    def move(self, start_pos, end_pos):
        """Abstract move method (to be overridden by subclasses)."""
        raise NotImplementedError("Move logic must be implemented by piece subclasses.")


class Pawn(ChessPiece):
    """Represents a Pawn."""
    def move(self, start_pos, end_pos):
        # Implement pawn movement rules:
        # - Can move forward 1 square (2 on first move)
        # - Can capture diagonally
        # - Add en passant and promotion logic
        pass


class Rook(ChessPiece):
    """Represents a Rook."""
    def move(self, start_pos, end_pos):
        # Implement rook movement rules:
        # - Can move horizontally and vertically any number of squares
        pass


class Knight(ChessPiece):
    """Represents a Knight."""
    def move(self, start_pos, end_pos):
        # Implement knight movement rules:
        # - Moves in L-shape (2 squares in one direction, 1 square perpendicular)
        pass


class Bishop(ChessPiece):
    """Represents a Bishop."""
    def move(self, start_pos, end_pos):
        # Implement bishop movement rules:
        # - Can move diagonally any number of squares
        pass


class Queen(ChessPiece):
    """Represents a Queen."""
    def move(self, start_pos, end_pos):
        # Implement queen movement rules:
        # - Can move horizontally, vertically, or diagonally any number of squares
        pass


class King(ChessPiece):
    """Represents a King."""
    def move(self, start_pos, end_pos):
        # Implement king movement rules:
        # - Can move one square in any direction
        # - Add castling logic
        pass
 

class Board:
    """Represents the 8x8 chess board."""
    def __init__(self):
        self.grid = self.create_board()

    def create_board(self):
        """Initialize an 8x8 board with pieces in their starting positions."""
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Place pawns
        for i in range(8):
            board[1][i] = Pawn("white")  # White pawns
            board[6][i] = Pawn("black")  # Black pawns

        # Place other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i in range(8):
            board[0][i] = piece_order[i]("white")  # White pieces
            board[7][i] = piece_order[i]("black")  # Black pieces
        
        return board

    def display(self):
        """Print the board in a human-readable format."""
        piece_symbols = {
            Pawn: 'P', Rook: 'R', Knight: 'N', 
            Bishop: 'B', Queen: 'Q', King: 'K'
        }
        for row in self.grid:
            pieces = []
            for piece in row:
                if piece is None:
                    pieces.append('.')
                else:
                    symbol = piece_symbols.get(type(piece), '?')
                    symbol = symbol.lower() if piece.color == 'black' else symbol
                    pieces.append(symbol)
            print(' '.join(pieces))


class Game:
    """Controls the game flow."""
    def __init__(self):
        self.board = Board()
        self.turn = "white"  # White moves first
        self.move_history = []

    def play(self):
        """Main game loop."""
        while not self.is_game_over():
            self.display_board()
            move = input(f"{self.turn}'s move (e.g. 'e2 e4'): ")
            if self.process_move(move):
                self.move_history.append(move)
                self.switch_turns()

    def is_game_over(self):
        """Check for checkmate or stalemate."""
        # TODO: Implement checkmate and stalemate detection
        # - Check if king is in check
        # - Check if any legal moves are available
        # - Check for insufficient material
        return False

    def process_move(self, move):
        """Process player moves."""
        try:
            start, end = move.split()
            start_pos = self.algebraic_to_coords(start)
            end_pos = self.algebraic_to_coords(end)
            
            piece = self.board.grid[start_pos[0]][start_pos[1]]
            if piece and piece.color == self.turn:
                # TODO: Validate move is legal
                # - Check if move follows piece rules
                # - Check if path is clear
                # - Check if move puts/leaves own king in check
                return True
        except:
            print("Invalid move format. Use algebraic notation (e.g. 'e2 e4')")
        return False

    def algebraic_to_coords(self, pos):
        """Convert algebraic notation (e.g. 'e4') to grid coordinates."""
        col = ord(pos[0].lower()) - ord('a')
        row = int(pos[1]) - 1
        return (row, col)

    def switch_turns(self):
        """Switch turns between white and black."""
        self.turn = "black" if self.turn == "white" else "white"

# If this script is run directly, start the game
if __name__ == "__main__":
    game = Game()
    game.play()
