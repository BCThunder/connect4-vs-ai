import random
import time
import sys
import io
from board import Connect4Board
from cpu_logic import get_ai_move, AI_CHIP, PLAYER_CHIP

class GameStats:
    def __init__(self):
        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0
        self.total_moves = 0
        self.total_time = 0
        self.move_times = []

    def print_stats(self, num_games, file=None):
        output = []
        output.append("\n" + "=" * 60)
        output.append("CONNECT 4 AI TEST RESULTS")
        output.append("=" * 60)
        output.append(f"Total Games Played: {num_games}")
        output.append(f"\nResults:")
        output.append(f"  Player (🔵) Wins: {self.player_wins} ({self.player_wins/num_games*100:.1f}%)")
        output.append(f"  AI (🔴) Wins:     {self.ai_wins} ({self.ai_wins/num_games*100:.1f}%)")
        output.append(f"  Draws:            {self.draws} ({self.draws/num_games*100:.1f}%)")
        output.append(f"\nPerformance:")
        output.append(f"  Total Moves: {self.total_moves}")
        output.append(f"  Avg Moves per Game: {self.total_moves/num_games:.1f}")
        output.append(f"  Total AI Thinking Time: {self.total_time:.2f}s")
        output.append(f"  Avg AI Time per Move: {sum(self.move_times)/len(self.move_times):.3f}s" if self.move_times else "  N/A")
        output.append(f"  Avg AI Time per Game: {self.total_time/num_games:.2f}s")
        output.append("=" * 60)

        result = "\n".join(output)
        print(result)
        if file:
            file.write(result + "\n")

def suppress_stdout(func):
    """Decorator to suppress stdout during function execution."""
    def wrapper(*args, **kwargs):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            result = func(*args, **kwargs)
        finally:
            sys.stdout = old_stdout
        return result
    return wrapper

def get_random_move(board):
    """Simple random player for testing."""
    valid_moves = board.getValidMoves()
    if valid_moves:
        return random.choice(valid_moves)
    return None

def get_smart_random_move(board):
    """Slightly smarter random player - blocks obvious wins and takes winning moves."""
    valid_moves = board.getValidMoves()

    # Check if we can win
    for move in valid_moves:
        test_board = board.clone()
        test_board.placePiece(move, PLAYER_CHIP)
        if test_board.checkWin(PLAYER_CHIP):
            return move

    # Check if we need to block AI from winning
    for move in valid_moves:
        test_board = board.clone()
        test_board.placePiece(move, AI_CHIP)
        if test_board.checkWin(AI_CHIP):
            return move

    # Otherwise, random move
    return random.choice(valid_moves)

def play_game(player_strategy="random", show_progress=False):
    """
    Play one game and return the result.

    Args:
        player_strategy: "random" or "smart_random"
        show_progress: if True, prints game number updates

    Returns:
        tuple: (winner, num_moves, ai_time, move_times)
               winner: "player", "ai", or "draw"
    """
    board = Connect4Board()
    turn = 0
    ai_time = 0
    move_times = []

    while True:
        if turn % 2 == 0:
            # Player's turn
            if player_strategy == "random":
                col = get_random_move(board)
            else:  # smart_random
                col = get_smart_random_move(board)

            if col is None:
                return ("draw", turn, ai_time, move_times)

            board.placePiece(col, PLAYER_CHIP)

            if board.checkWin(PLAYER_CHIP):
                return ("player", turn + 1, ai_time, move_times)
        else:
            # AI's turn (suppress AI's print statements)
            start = time.time()
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            try:
                col = get_ai_move(board)
            finally:
                sys.stdout = old_stdout
            elapsed = time.time() - start
            ai_time += elapsed
            move_times.append(elapsed)

            if col is None:
                return ("draw", turn, ai_time, move_times)

            board.placePiece(col, AI_CHIP)

            if board.checkWin(AI_CHIP):
                return ("ai", turn + 1, ai_time, move_times)

        turn += 1

        # Check for draw
        if len(board.getValidMoves()) == 0:
            return ("draw", turn, ai_time, move_times)

def play_ai_vs_ai_game(show_progress=False):
    """
    Play one game where both players are AI.

    Returns:
        tuple: (winner, num_moves, total_time, move_times)
               winner: "first" (🔵), "second" (🔴), or "draw"
    """
    board = Connect4Board()
    turn = 0
    total_time = 0
    move_times = []

    while True:
        start = time.time()

        # Suppress AI print statements
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            if turn % 2 == 0:
                # First AI (plays as PLAYER_CHIP)
                col = get_ai_move_for_chip(board, PLAYER_CHIP)
                chip = PLAYER_CHIP
                winner_name = "first"
            else:
                # Second AI (plays as AI_CHIP)
                col = get_ai_move(board)
                chip = AI_CHIP
                winner_name = "second"
        finally:
            sys.stdout = old_stdout

        elapsed = time.time() - start
        total_time += elapsed
        move_times.append(elapsed)

        if col is None:
            return ("draw", turn, total_time, move_times)

        board.placePiece(col, chip)

        if board.checkWin(chip):
            return (winner_name, turn + 1, total_time, move_times)

        turn += 1

        # Check for draw
        if len(board.getValidMoves()) == 0:
            return ("draw", turn, total_time, move_times)

def get_ai_move_for_chip(board, chip):
    """Modified AI move that plays for a specific chip."""
    import math

    def evaluate_for_chip(board, chip):
        score = 0
        center_col = 3
        center_count = sum(1 for r in range(6) if board.board[r][center_col] == chip)
        score += center_count * 3
        return score

    def minimax_for_chip(board, depth, maximizing, player_chip, opponent_chip):
        if board.checkWin(player_chip):
            return (None, 100000)
        if board.checkWin(opponent_chip):
            return (None, -100000)
        if depth == 0 or len(board.getValidMoves()) == 0:
            return (None, evaluate_for_chip(board, player_chip))

        if maximizing:
            best_score = -math.inf
            best_move = None
            for move in board.getValidMoves():
                test = board.clone()
                test.placePiece(move, player_chip)
                _, score = minimax_for_chip(test, depth - 1, False, player_chip, opponent_chip)
                if score > best_score:
                    best_score = score
                    best_move = move
            return (best_move, best_score)
        else:
            best_score = math.inf
            best_move = None
            for move in board.getValidMoves():
                test = board.clone()
                test.placePiece(move, opponent_chip)
                _, score = minimax_for_chip(test, depth - 1, True, player_chip, opponent_chip)
                if score < best_score:
                    best_score = score
                    best_move = move
            return (best_move, best_score)

    opponent_chip = AI_CHIP if chip == PLAYER_CHIP else PLAYER_CHIP
    move, _ = minimax_for_chip(board, depth=4, maximizing=True, player_chip=chip, opponent_chip=opponent_chip)
    return move

def run_tests(num_games=100, player_strategy="random", mode="player_vs_ai", output_file=None):
    """
    Run multiple test games.

    Args:
        num_games: number of games to play
        player_strategy: "random" or "smart_random" (only for player_vs_ai mode)
        mode: "player_vs_ai" or "ai_vs_ai"
        output_file: file object to write output to (optional)
    """
    stats = GameStats()

    header = f"\nStarting {num_games} games of Connect 4..."
    mode_info = f"Mode: {mode}"
    strategy_info = f"Player Strategy: {player_strategy}" if mode == "player_vs_ai" else ""
    progress_header = "\nProgress:"

    print(header)
    print(mode_info)
    if strategy_info:
        print(strategy_info)
    print(progress_header)

    if output_file:
        output_file.write(header + "\n")
        output_file.write(mode_info + "\n")
        if strategy_info:
            output_file.write(strategy_info + "\n")
        output_file.write(progress_header + "\n")

    for i in range(num_games):
        if (i + 1) % 10 == 0:
            progress = f"  Completed {i + 1}/{num_games} games..."
            print(progress)
            if output_file:
                output_file.write(progress + "\n")

        if mode == "ai_vs_ai":
            winner, moves, ai_time, move_times = play_ai_vs_ai_game()
            if winner == "first":
                stats.player_wins += 1
            elif winner == "second":
                stats.ai_wins += 1
            else:
                stats.draws += 1
        else:
            winner, moves, ai_time, move_times = play_game(player_strategy)
            if winner == "player":
                stats.player_wins += 1
            elif winner == "ai":
                stats.ai_wins += 1
            else:
                stats.draws += 1

        stats.total_moves += moves
        stats.total_time += ai_time
        stats.move_times.extend(move_times)

    stats.print_stats(num_games, output_file)

def run_all_tests(num_games=100, output_filename="test_results.txt"):
    """
    Run all test suites and output results to a file.

    Args:
        num_games: number of games to play for each test suite
        output_filename: name of the file to write results to
    """
    import datetime

    with open(output_filename, 'w') as f:
        # Write header
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"""
{'=' * 70}
CONNECT 4 AI - COMPREHENSIVE TEST SUITE RESULTS
{'=' * 70}
Test Run Date: {timestamp}
Games per Test Suite: {num_games}
{'=' * 70}
"""
        print(header)
        f.write(header + "\n")

        # Test 1: AI vs Random Player
        separator = f"\n\n{'#' * 70}\n# TEST SUITE 1: AI vs Random Player\n{'#' * 70}\n"
        print(separator)
        f.write(separator + "\n")
        run_tests(num_games, "random", "player_vs_ai", f)

        # Test 2: AI vs Smart Random Player
        separator = f"\n\n{'#' * 70}\n# TEST SUITE 2: AI vs Smart Random Player\n{'#' * 70}\n"
        print(separator)
        f.write(separator + "\n")
        run_tests(num_games, "smart_random", "player_vs_ai", f)

        # Test 3: AI vs AI
        separator = f"\n\n{'#' * 70}\n# TEST SUITE 3: AI vs AI\n{'#' * 70}\n"
        print(separator)
        f.write(separator + "\n")
        run_tests(num_games, "random", "ai_vs_ai", f)

        # Write footer
        footer = f"""
\n{'=' * 70}
ALL TESTS COMPLETED
{'=' * 70}
Results saved to: {output_filename}
"""
        print(footer)
        f.write(footer + "\n")

def main():
    print("Connect 4 AI Testing Suite")
    print("=" * 60)
    print("\nChoose test mode:")
    print("1. AI vs Random Player (100 games)")
    print("2. AI vs Smart Random Player (100 games)")
    print("3. AI vs AI (100 games)")
    print("4. Run ALL test suites and save to file")
    print("5. Custom test")

    choice = input("\nEnter choice (1-5): ").strip()

    if choice == "1":
        run_tests(100, "random", "player_vs_ai")
    elif choice == "2":
        run_tests(100, "smart_random", "player_vs_ai")
    elif choice == "3":
        run_tests(100, "random", "ai_vs_ai")
    elif choice == "4":
        num_games = input("Number of games per test suite (default 100): ").strip()
        num_games = int(num_games) if num_games else 100
        filename = input("Output filename (default test_results.txt): ").strip()
        filename = filename if filename else "test_results.txt"
        run_all_tests(num_games, filename)
    elif choice == "5":
        num_games = int(input("Number of games: "))
        mode = input("Mode (player_vs_ai or ai_vs_ai): ").strip()
        if mode == "player_vs_ai":
            strategy = input("Player strategy (random or smart_random): ").strip()
            run_tests(num_games, strategy, mode)
        else:
            run_tests(num_games, "random", mode)
    else:
        print("Invalid choice. Running default test (100 games vs random player)...")
        run_tests(100, "random", "player_vs_ai")

if __name__ == "__main__":
    main()
