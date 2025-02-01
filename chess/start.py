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
        # Pawn-specific movement logic goes here
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
        
        return board

    def display(self):
        """Print the board in a human-readable format."""
        for row in self.grid:
            print(" ".join([str(piece) if piece else "." for piece in row]))


class Game:
    """Controls the game flow."""
    def __init__(self):
        self.board = Board()
        self.turn = "white"  # White moves first

    def play(self):
        """Main game loop."""
        while not self.is_game_over():
            self.display_board()
            move = input(f"{self.turn}'s move: ")
            self.process_move(move)
            self.switch_turns()

    def is_game_over(self):
        """Check for checkmate or stalemate."""
        return False  # Placeholder

    def process_move(self, move):
        """Process player moves."""
        pass

    def switch_turns(self):
        """Switch turns between white and black."""
        self.turn = "black" if self.turn == "white" else "white"

# If this script is run directly, start the game
if __name__ == "__main__":
    game = Game()
    game.play()