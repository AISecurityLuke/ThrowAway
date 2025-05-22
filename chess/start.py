import copy

# Future Enhancements & GUI Integration:
# In upcoming iterations, we plan to expand this into a full-fledged chess game.
# For a simple GUI, consider using libraries such as:
# - tkinter (built-in with Python, suitable for basic interfaces)
# - pygame (for more dynamic graphics and interactive gameplay)
# - Alternatively, PyQt or wxPython for advanced features.
#
# Additional features to be built out include:
# - Comprehensive move validation (path clearance, check and checkmate detection, castling rules, etc.)
# - AI opponents and game state management.
# - Enhanced GUI integration to replace command-line inputs.

class ChessPiece:
    """Base class for all chess pieces."""
    def __init__(self, color):
        self.color = color  # 'white' or 'black'
        self.has_moved = False  # Track if a piece has moved (useful for castling and pawn's initial two-step)

    def move(self, start_pos, end_pos):
        """Abstract move method (to be overridden by piece subclasses)."""
        raise NotImplementedError("Move logic must be implemented by piece subclasses.")


class Pawn(ChessPiece):
    """Represents a Pawn."""
    def move(self, start_pos, end_pos):
        # Implement pawn movement rules:
        # - Can move forward 1 square (or 2 on its first move)
        # - Can capture diagonally
        # - TODO: Implement detailed en passant and promotion logic (promotion is handled post-move)
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        direction = 1 if self.color == "white" else -1

        # Normal forward move
        if dy == 0:
            if dx == direction:
                return True
            # Allow two-square move from starting position if pawn hasn't moved
            if (not self.has_moved and
                ((self.color == "white" and start_pos[0] == 1) or 
                 (self.color == "black" and start_pos[0] == 6)) and dx == 2 * direction):
                return True

        # Diagonal capture
        if abs(dy) == 1 and dx == direction:
            return True

        return False

    def attacks(self, start_pos, end_pos):
        # Pawn attacks differ from its normal forward move.
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        direction = 1 if self.color == "white" else -1
        return dx == direction and abs(dy) == 1


class Rook(ChessPiece):
    """Represents a Rook."""
    def move(self, start_pos, end_pos):
        # Implement rook movement rules:
        # - Can move horizontally and vertically any number of squares
        if start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1]:
            return True
        return False


class Knight(ChessPiece):
    """Represents a Knight."""
    def move(self, start_pos, end_pos):
        # Implement knight movement rules:
        # - Moves in an L-shape (2 squares in one direction, 1 square perpendicular)
        dx = abs(end_pos[0] - start_pos[0])
        dy = abs(end_pos[1] - start_pos[1])
        if (dx, dy) in [(2, 1), (1, 2)]:
            return True
        return False


class Bishop(ChessPiece):
    """Represents a Bishop."""
    def move(self, start_pos, end_pos):
        # Implement bishop movement rules:
        # - Can move diagonally any number of squares
        if abs(end_pos[0] - start_pos[0]) == abs(end_pos[1] - start_pos[1]) and (end_pos[0] - start_pos[0]) != 0:
            return True
        return False


class Queen(ChessPiece):
    """Represents a Queen."""
    def move(self, start_pos, end_pos):
        # Implement queen movement rules:
        # - Can move horizontally, vertically, or diagonally any number of squares
        if start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1]:
            return True
        if abs(end_pos[0] - start_pos[0]) == abs(end_pos[1] - start_pos[1]) and (end_pos[0] - start_pos[0]) != 0:
            return True
        return False


class King(ChessPiece):
    """Represents a King."""
    def move(self, start_pos, end_pos):
        # Implement king movement rules:
        # - Can move one square in any direction
        # - Castling: move two squares horizontally if the king hasn't moved
        dx = abs(end_pos[0] - start_pos[0])
        dy = abs(end_pos[1] - start_pos[1])
        # Normal king move: one square any direction
        if dx <= 1 and dy <= 1 and (dx != 0 or dy != 0):
            return True
        # Castling move (allow kingside or queenside) if king hasn't moved yet
        if dx == 0 and abs(dy) == 2 and not self.has_moved:
            return True
        return False
  

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

        # Place other pieces in standard order
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
    
    def is_path_clear(self, start_pos, end_pos):
        """Check if the path between start_pos and end_pos is clear of obstructions.
        
        This method assumes a linear (horizontal, vertical, or diagonal) move.
        """
        row_diff = end_pos[0] - start_pos[0]
        col_diff = end_pos[1] - start_pos[1]
        step_row = (row_diff > 0) - (row_diff < 0)
        step_col = (col_diff > 0) - (col_diff < 0)
        
        current_row = start_pos[0] + step_row
        current_col = start_pos[1] + step_col
        
        # Traverse the path until reaching the destination (excluding end_pos)
        while (current_row, current_col) != end_pos:
            if self.grid[current_row][current_col] is not None:
                return False
            current_row += step_row
            current_col += step_col
        return True

    def find_king(self, color):
        """Locate the king of the specified color on the board."""
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if piece and isinstance(piece, King) and piece.color == color:
                    return (i, j)
        return None

    def is_square_attacked(self, pos, by_color):
        """Determine if a given square is attacked by any piece of the specified color."""
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if piece and piece.color == by_color:
                    if isinstance(piece, Pawn):
                        if piece.attacks((i, j), pos):
                            return True
                    elif isinstance(piece, Knight):
                        if piece.move((i, j), pos):
                            return True
                    else:
                        if piece.move((i, j), pos) and self.is_path_clear((i, j), pos):
                            return True
        return False

    def is_in_check(self, color):
        """Check if the king of the specified color is under attack."""
        king_pos = self.find_king(color)
        if king_pos is None:
            return False
        opponent_color = "black" if color == "white" else "white"
        return self.is_square_attacked(king_pos, opponent_color)


class Game:
    """Controls the game flow."""
    def __init__(self):
        self.board = Board()
        self.turn = "white"  # White moves first
        self.move_history = []
        self.vs_ai = False  # Flag to indicate playing against AI
        self.ai_color = None  # Which color the AI controls (if any)
        self.human_color = None  # The human player's chosen color (if vs_ai)
        self.game_over_auto_reset_scheduled = False  # Ensure auto–reset is scheduled only once
        # TODO: Initialize and integrate advanced GUI components (e.g., tkinter or pygame) in future revisions

    def play(self):
        """Main game loop for CLI play."""
        while not self.is_game_over():
            self.board.display()
            # If playing versus AI and it's AI's turn, then let the AI move.
            if self.vs_ai and self.turn == self.ai_color:
                print(f"AI ({self.ai_color}) is making a move...")
                self.ai_move()
                continue
            move = input(f"{self.turn}'s move (e.g. 'e2 e4'): ")
            if self.process_move(move):
                self.move_history.append(move)
                self.switch_turns()

    def launch_gui(self):
        """Launch a basic interactive GUI using tkinter for chess game."""
        try:
            import tkinter as tk
            from tkinter import messagebox, simpledialog
        except ImportError:
            print("tkinter is not available. Falling back to CLI mode.")
            self.play()
            return
        
        self.is_gui = True  # flag indicating GUI mode
        self.selected_square = None  # store selected GUI square (r, c) in grid coordinates
        self.window = tk.Tk()
        self.window.title("Chess Game GUI")
        
        # Create board frame
        self.board_frame = tk.Frame(self.window)
        self.board_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Create an 8x8 grid of buttons.
        # If playing vs AI and human is black, show board with black's perspective,
        # otherwise default (white at bottom).
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        for r in range(8):
            for c in range(8):
                if self.vs_ai and hasattr(self, 'human_color') and self.human_color == 'black':
                    board_row = r
                else:
                    board_row = 7 - r
                bg_color = "#F0D9B5" if ((board_row + c) % 2 == 0) else "#B58863"
                btn = tk.Button(self.board_frame, text="", width=4, height=2, font=("Arial", 24),
                                bg=bg_color,
                                command=lambda r=r, c=c: self.on_square_click(r, c))
                btn.grid(row=r, column=c)
                self.squares[r][c] = btn
        
        # Message label to show status updates
        self.message_label = tk.Label(self.window, text=f"{self.turn.capitalize()}'s turn", font=("Arial", 14))
        self.message_label.grid(row=1, column=0, pady=5)
        
        # Reset button to restart the game
        reset_button = tk.Button(self.window, text="Reset Game", command=self.reset_game)
        reset_button.grid(row=2, column=0, pady=5)
        
        self.update_gui()
        # Start periodic check for AI moves (turn loop)
        self.window.after(500, self.check_ai)
        self.window.mainloop()

    def is_game_over(self):
        """Check for checkmate or stalemate.
        
        Future implementation should:
        - Check if the king is in check.
        - Evaluate if any legal moves are available.
        - Account for insufficient material conditions.
        """
        valid_moves = self.get_valid_moves(self.turn)
        if not valid_moves:
            if self.board.is_in_check(self.turn):
                result = f"Checkmate! {'white' if self.turn == 'black' else 'black'} wins!"
            else:
                result = "Stalemate!"
            print(result)
            if hasattr(self, 'message_label'):
                self.message_label.config(text=result)
            # If in GUI mode and auto-reset hasn't been scheduled yet, schedule a reset in 10 seconds.
            if getattr(self, 'is_gui', False) and not self.game_over_auto_reset_scheduled:
                self.game_over_auto_reset_scheduled = True
                self.window.after(10000, self.reset_game)
            return True
        return False

    def process_move(self, move, ai_move=False, suppress_output=False):
        """Process player moves using algebraic notation and validate moves further."""
        try:
            start, end = move.split()
            start_pos = self.algebraic_to_coords(start)
            end_pos = self.algebraic_to_coords(end)
            
            piece = self.board.grid[start_pos[0]][start_pos[1]]
            if not piece or piece.color != self.turn:
                if not suppress_output:
                    print("No piece at the starting position or it is not your turn.")
                return False

            # Additional validations for Pawn moves
            if isinstance(piece, Pawn):
                if start_pos[1] == end_pos[1]:
                    # Forward move: target square must be empty
                    if self.board.grid[end_pos[0]][end_pos[1]] is not None:
                        if not suppress_output:
                            print("Pawn cannot move forward into an occupied square.")
                        return False
                else:
                    # Diagonal move: must capture an opponent's piece
                    target = self.board.grid[end_pos[0]][end_pos[1]]
                    if target is None or target.color == piece.color:
                        if not suppress_output:
                            print("Invalid diagonal move for Pawn.")
                        return False
            else:
                # For other pieces, disallow capturing your own piece
                target = self.board.grid[end_pos[0]][end_pos[1]]
                if target is not None and target.color == piece.color:
                    if not suppress_output:
                        print("Cannot capture your own piece.")
                    return False

            # Check if the piece's movement rules allow the move
            if not piece.move(start_pos, end_pos):
                if not suppress_output:
                    print("Illegal move according to piece rules.")
                return False

            # Use a deepcopy of the board to simulate the move
            new_board = copy.deepcopy(self.board)
            sim_piece = new_board.grid[start_pos[0]][start_pos[1]]

            # Special handling for castling with the King
            if isinstance(sim_piece, King) and abs(end_pos[1] - start_pos[1]) == 2:
                # Determine castling side
                if end_pos[1] - start_pos[1] > 0:
                    # Kingside castling: move the rook from the corner to just left of the king's destination
                    rook_pos = (start_pos[0], 7)
                    new_rook_pos = (start_pos[0], 5)
                else:
                    # Queenside castling: move the rook from the corner to just right of the king's destination
                    rook_pos = (start_pos[0], 0)
                    new_rook_pos = (start_pos[0], 3)
                
                rook = new_board.grid[rook_pos[0]][rook_pos[1]]
                if not rook or not isinstance(rook, Rook) or rook.color != sim_piece.color or rook.has_moved:
                    if not suppress_output:
                        print("Castling not permitted: Rook is not in position or has already moved.")
                    return False
                
                # Ensure the path between the king and rook is clear
                if not new_board.is_path_clear(start_pos, rook_pos):
                    if not suppress_output:
                        print("Castling not permitted: Path is obstructed.")
                    return False

                # Ensure the king is not currently in check and does not pass
                # through check while castling.
                if self.board.is_in_check(self.turn):
                    if not suppress_output:
                        print("Castling not permitted: King is in check.")
                    return False

                step = 1 if end_pos[1] > start_pos[1] else -1
                temp_board = copy.deepcopy(self.board)
                temp_board.grid[start_pos[0]][start_pos[1]] = None
                temp_board.grid[start_pos[0]][start_pos[1] + step] = copy.deepcopy(sim_piece)
                if temp_board.is_in_check(self.turn):
                    if not suppress_output:
                        print("Castling not permitted: Path is under attack.")
                    return False

                # Move the king and the rook as part of the castling maneuver
                new_board.grid[end_pos[0]][end_pos[1]] = sim_piece
                new_board.grid[start_pos[0]][start_pos[1]] = None
                new_board.grid[new_rook_pos[0]][new_rook_pos[1]] = rook
                new_board.grid[rook_pos[0]][rook_pos[1]] = None
                sim_piece.has_moved = True
                rook.has_moved = True
            else:
                # For non-castling moves (excluding Knight jumps), check if the path is clear.
                if not isinstance(sim_piece, Knight) and not new_board.is_path_clear(start_pos, end_pos):
                    if not suppress_output:
                        print("The path is obstructed.")
                    return False

                # Move is valid; update the board for the moving piece
                new_board.grid[end_pos[0]][end_pos[1]] = sim_piece
                new_board.grid[start_pos[0]][start_pos[1]] = None
                sim_piece.has_moved = True

                # Pawn promotion: if a pawn reaches the last row, prompt for promotion.
                if isinstance(sim_piece, Pawn) and ((sim_piece.color == "white" and end_pos[0] == 7) or
                                                    (sim_piece.color == "black" and end_pos[0] == 0)):
                    if ai_move:
                        promotion_choice = 'Q'
                    else:
                        try:
                            from tkinter import simpledialog
                        except ImportError:
                            simpledialog = None
                        if hasattr(self, 'is_gui') and self.is_gui and simpledialog:
                            promotion_choice = simpledialog.askstring("Pawn Promotion", "Promote pawn to (Q, R, B, N):")
                            promotion_choice = promotion_choice.upper().strip() if promotion_choice else 'Q'
                        else:
                            promotion_choice = input("Pawn reached the end! Promote to (Q, R, B, N): ").upper().strip()
                    if promotion_choice == 'Q':
                        sim_piece = Queen(sim_piece.color)
                    elif promotion_choice == 'R':
                        sim_piece = Rook(sim_piece.color)
                    elif promotion_choice == 'B':
                        sim_piece = Bishop(sim_piece.color)
                    elif promotion_choice == 'N':
                        sim_piece = Knight(sim_piece.color)
                    else:
                        if not suppress_output:
                            print("Invalid promotion choice. Defaulting to Queen.")
                        sim_piece = Queen(sim_piece.color)
                    sim_piece.has_moved = True
                    new_board.grid[end_pos[0]][end_pos[1]] = sim_piece

            # Check if the move puts the player's own king in check
            if new_board.is_in_check(self.turn):
                if not suppress_output:
                    print("Move illegal: cannot leave king in check.")
                return False

            # If the move places the opponent in check, notify the player
            opponent = "black" if self.turn == "white" else "white"
            if new_board.is_in_check(opponent):
                if not suppress_output:
                    print(f"Check to {opponent}!")

            self.board = new_board
            return True
        except Exception:
            if not suppress_output:
                print("Invalid move format. Use algebraic notation (e.g. 'e2 e4')")
            return False

    def algebraic_to_coords(self, pos):
        """Convert algebraic notation (e.g. 'e4') to grid coordinates (row, col)."""
        col = ord(pos[0].lower()) - ord('a')
        row = int(pos[1]) - 1
        return (row, col)

    def switch_turns(self):
        """Switch turns between white and black."""
        self.turn = "black" if self.turn == "white" else "white"

    def on_square_click(self, gui_r, gui_c):
        """Handle a click on a GUI square. (gui_r, gui_c) are the grid positions."""
        if self.is_game_over():
            self.message_label.config(text="Game Over!")
            return
        # If playing versus AI, only allow moves when it's the human's turn.
        if self.vs_ai and self.turn != self.human_color:
            self.message_label.config(text="Not your turn.")
            return
        # Map GUI grid coordinates to board coordinates based on human's color.
        if self.vs_ai and hasattr(self, 'human_color') and self.human_color == 'black':
            board_r = gui_r
        else:
            board_r = 7 - gui_r
        board_c = gui_c
        import tkinter as tk  # for any color constants
        
        if self.selected_square is None:
            piece = self.board.grid[board_r][board_c]
            if not piece or piece.color != self.turn:
                self.message_label.config(text="Invalid selection. Select your own piece.")
                return
            # Mark this square as selected and highlight it.
            self.selected_square = (gui_r, gui_c)
            self.squares[gui_r][gui_c].config(bg="yellow")
            self.message_label.config(text=f"Selected {chr(board_c + ord('a'))}{board_r+1}")
        else:
            # A piece has been selected; this click is the destination.
            sel_gui_r, sel_gui_c = self.selected_square
            if self.vs_ai and hasattr(self, 'human_color') and self.human_color == 'black':
                src_board_r = sel_gui_r
            else:
                src_board_r = 7 - sel_gui_r
            src_board_c = sel_gui_c
            # Convert to algebraic notation (e.g., 'e2')
            src_alg = f"{chr(src_board_c + ord('a'))}{src_board_r+1}"
            dst_alg = f"{chr(board_c + ord('a'))}{board_r+1}"
            move_str = f"{src_alg} {dst_alg}"
            # Reset highlight of the previously selected square.
            original_bg = "#F0D9B5" if ((src_board_r + src_board_c) % 2 == 0) else "#B58863"
            self.squares[sel_gui_r][sel_gui_c].config(bg=original_bg)
            self.selected_square = None
            
            # Process the move.
            if self.process_move(move_str):
                self.move_history.append(move_str)
                self.switch_turns()
                self.message_label.config(text=f"Move {src_alg} to {dst_alg} accepted. {self.turn.capitalize()}'s turn.")
            else:
                self.message_label.config(text="Illegal move. Try again.")
            self.update_gui()

    def update_gui(self):
        """Update the GUI board to reflect the current state of the game."""
        for r in range(8):
            for c in range(8):
                if self.vs_ai and hasattr(self, 'human_color') and self.human_color == 'black':
                    board_row = r
                else:
                    board_row = 7 - r
                piece = self.board.grid[board_row][c]
                symbol = self.get_piece_symbol(piece)
                self.squares[r][c].config(text=symbol)
                # Reset the square's background color.
                bg_color = "#F0D9B5" if ((board_row + c) % 2 == 0) else "#B58863"
                self.squares[r][c].config(bg=bg_color)

    def get_piece_symbol(self, piece):
        """Return a Unicode symbol representing the chess piece."""
        if piece is None:
            return ""
        symbols_white = {
            Pawn: "♙",
            Rook: "♖",
            Knight: "♘",
            Bishop: "♗",
            Queen: "♕",
            King: "♔"
        }
        symbols_black = {
            Pawn: "♟",
            Rook: "♜",
            Knight: "♞",
            Bishop: "♝",
            Queen: "♛",
            King: "♚"
        }
        if piece.color == "white":
            return symbols_white.get(type(piece), "?")
        else:
            return symbols_black.get(type(piece), "?")

    def reset_game(self):
        """Reset the game state to start a new game."""
        self.board = Board()
        self.turn = "white"
        self.move_history = []
        self.selected_square = None
        self.game_over_auto_reset_scheduled = False
        self.update_gui()
        if hasattr(self, 'message_label'):
            self.message_label.config(text="New game started. White's turn.")

    def try_move(self, move_str, ai_move=False):
        """Simulate a move without permanently changing the game state."""
        saved_board = copy.deepcopy(self.board)
        saved_turn = self.turn
        result = self.process_move(move_str, ai_move=ai_move, suppress_output=True)
        self.board = saved_board
        self.turn = saved_turn
        return result

    def get_valid_moves(self, color):
        """Return a list of valid moves (algebraic notation) for the specified color."""
        valid_moves = []
        saved_board = copy.deepcopy(self.board)
        saved_turn = self.turn
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.color == color:
                    src_alg = f"{chr(col + ord('a'))}{row+1}"
                    for r in range(8):
                        for c in range(8):
                            dst_alg = f"{chr(c + ord('a'))}{r+1}"
                            move_str = f"{src_alg} {dst_alg}"
                            if self.try_move(move_str, ai_move=True):
                                valid_moves.append(move_str)
        self.board = saved_board
        self.turn = saved_turn
        return valid_moves

    # AI starts here
    def ai_move(self):
        """Perform a very simple AI move by selecting a random valid move."""
        import random
        valid_moves = self.get_valid_moves(self.ai_color)
        if not valid_moves:
            print("AI has no valid moves. Stalemate?")
            return
        move_str = random.choice(valid_moves)
        print(f"AI ({self.ai_color}) moves: {move_str}")
        self.process_move(move_str, ai_move=True)
        self.move_history.append(move_str)
        self.switch_turns()
        if hasattr(self, 'update_gui'):
            self.update_gui()

    def check_ai(self):
        """Periodically checks if it's the AI's turn and makes a move if so."""
        if self.is_game_over():
            return
        if self.vs_ai and self.turn == self.ai_color:
            self.ai_move()
        self.window.after(500, self.check_ai)

# If this script is run directly, start the game
if __name__ == "__main__":
    game = Game()
    mode = input("Select game mode - (1) CLI or (2) GUI: ").strip()
    ai_choice = input("Play against AI? (Y/N): ").strip().upper()
    if ai_choice == "Y":
        game.vs_ai = True
        while True:
            player_color = input("Choose your color (white/black): ").strip().lower()
            if player_color in ("white", "black"):
                break
        game.ai_color = "black" if player_color == "white" else "white"
        # Ensure that white always starts; if you choose black, AI (white) starts.
        game.turn = "white"
        game.human_color = player_color
    if mode == "2":
        game.launch_gui()
    else:
        game.play()
