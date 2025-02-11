import pygame
import chess
import chess.engine
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
WHITE = (238, 238, 210)
BROWN = (118, 150, 86)
HIGHLIGHT_COLOR = (0, 255, 0)  # Green highlight for legal moves

# Load Stockfish Engine (Update the path)
STOCKFISH_PATH = r"G:\Ai-bot Chess\stockfish\stockfish.exe"  # Make sure this path is correct
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

# Initialize Board
board = chess.Board()

# Get the directory of the current script
base_path = os.path.dirname(__file__)  # This gives you the directory where the script is located

# Load Images
piece_images = {}
for piece in ["p", "n", "b", "r", "q", "k"]:  # Loop through each piece
    for color in ["w", "b"]:  # For both white and black pieces
        # Construct the image path using the base path and the 'images' folder
        image_path = os.path.join(base_path, "image", f"{color}{piece.upper()}.png")
        
        # Ensure the image file exists before trying to load it
        if os.path.exists(image_path):
            piece_images[color + piece.upper()] = pygame.transform.scale(
                pygame.image.load(image_path), (SQUARE_SIZE, SQUARE_SIZE)
            )
        else:
            print(f"Error: {image_path} does not exist!")

# Create Pygame Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess with Stockfish AI")

def draw_board():
    """Draw the chessboard."""
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    """Draw pieces based on the board state."""
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(chess.square(col, 7 - row))  # Convert board to screen coordinates
            if piece:
                piece_symbol = piece.symbol()
                color = "w" if piece_symbol.isupper() else "b"
                screen.blit(piece_images[color + piece_symbol.upper()], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_possible_moves(legal_moves):
    """Draw the legal moves for a selected piece."""
    for move in legal_moves:
        row, col = divmod(move, 8)  # Convert move index to row and column
        pygame.draw.circle(screen, HIGHLIGHT_COLOR, 
                           (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

def get_square(mouse_pos):
    """Convert mouse position to board square."""
    x, y = mouse_pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)  # Convert screen to board coordinates
    return chess.square(col, row)

def get_stockfish_move():
    """Get the best move from Stockfish."""
    result = engine.play(board, chess.engine.Limit(time=1.0))
    return result.move

# Game Loop
selected_square = None
possible_moves = []
running = True
player_turn = True  # Player starts the game

while running:
    draw_board()
    draw_pieces()

    # Draw possible moves if a piece is selected and it's the player's turn
    if selected_square is not None and player_turn:
        piece = board.piece_at(selected_square)
        if piece and board.color_at(selected_square) == chess.WHITE:  # Only highlight for white pieces (player)
            legal_moves = [move for move in board.legal_moves if move.from_square == selected_square]
            possible_moves = [move.to_square for move in legal_moves]
            draw_possible_moves(possible_moves)
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            square = get_square(event.pos)

            if selected_square is None and player_turn:
                # Player selects a piece (only allow the player to select their own pieces)
                if board.piece_at(square) and board.color_at(square) == chess.WHITE:
                    selected_square = square
                    possible_moves = []  # Reset possible moves when selecting a new piece
            else:
                # If clicked on a valid move for the player
                if square in possible_moves:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)  # User makes a move
                        selected_square = None
                        possible_moves = []  # Reset possible moves

                        # End player turn and start AI turn
                        player_turn = False

                        # Stockfish's turn (only if game isn't over)
                        if not board.is_game_over():
                            stockfish_move = get_stockfish_move()
                            board.push(stockfish_move)  # Stockfish makes a move
                            player_turn = True  # Switch back to player's turn

                selected_square = None
                possible_moves = []  # Reset possible moves if user clicks somewhere else

pygame.quit()
engine.quit()
