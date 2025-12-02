import math
import time
from board import Connect4Board

AI_CHIP = "🔴"
PLAYER_CHIP = "🔵"

def evaluate(board: Connect4Board):
    """Simple heuristic: score positions where AI has potential wins."""
    score = 0
    # Center column preference
    center_col = 3
    center_count = sum(1 for r in range(6) if board.board[r][center_col] == AI_CHIP)
    score += center_count * 3
    return score

def minimax(board, depth, maximizing):
    # Terminal checks
    if board.checkWin(AI_CHIP):
        return (None, 100000)
    if board.checkWin(PLAYER_CHIP):
        return (None, -100000)
    if depth == 0 or len(board.getValidMoves()) == 0:
        return (None, evaluate(board))
    
    if maximizing:
        best_score = -math.inf
        best_move = None
        for move in board.getValidMoves():
            test = board.clone()
            test.placePiece(move, AI_CHIP)
            _, score = minimax(test, depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = move
        return (best_move, best_score)
    else:
        best_score = math.inf
        best_move = None
        for move in board.getValidMoves():
            test = board.clone()
            test.placePiece(move, PLAYER_CHIP)
            _, score = minimax(test, depth - 1, True)
            if score < best_score:
                best_score = score
                best_move = move
        return (best_move, best_score)

def get_ai_move(board: Connect4Board):
    start_time = time.time()
    move, score = minimax(board, depth=4, maximizing=True)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"CPU thinking... (took {elapsed_time:.3f} seconds)")
    print(f"Selected column: {move}, Score: {score}")
    
    return move