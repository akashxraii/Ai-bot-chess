import chess
import chess.engine

# Path to Stockfish Engine (Update this to your Stockfish binary)
STOCKFISH_PATH = "G:\Ai-bot Chess\stockfish"

# Initialize Stockfish engine
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

# Create a new chessboard
board = chess.Board()

def play_game():
    """Runs a simple chess game where the player plays against Stockfish."""
    while not board.is_game_over():
        print("\nCurrent Board:")
        print(board)

        # Get user move
        move = input("\nYour move (e.g., e2e4): ")
        if move in [m.uci() for m in board.legal_moves]:
            board.push_uci(move)
        else:
            print("Invalid move! Try again.")
            continue

        # Stockfish Move
        result = engine.play(board, chess.engine.Limit(time=1.0))
        board.push(result.move)
        print(f"\nStockfish Move: {result.move}")

    print("\nGame Over! Result:", board.result())
    engine.quit()

if __name__ == "__main__":
    play_game()
