from board import Connect4Board
from player import get_player_move
from cpu_logic import get_ai_move, AI_CHIP, PLAYER_CHIP

def main():
    board = Connect4Board()
    turn = 0

    print("Welcome to Connect Four!\n")

    while True:
        board.printBoard()

        if turn % 2 == 0:
            # Player
            col = get_player_move(board)
            board.placePiece(col, PLAYER_CHIP)

            if board.checkWin(PLAYER_CHIP):
                board.printBoard()
                print("\nGame Over! 🔵 Wins!")
                break
        else:
            col = get_ai_move(board)
            board.placePiece(col, AI_CHIP)

            if board.checkWin(AI_CHIP):
                board.printBoard()
                print("\nGame Over! 🔴 Wins!")
                break

        turn += 1

        if len(board.getValidMoves()) == 0:
            board.printBoard()
            print("\nGame Over! It's a draw.")
            break


if __name__ == "__main__":
    main()
