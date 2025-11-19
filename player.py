possibleLetters = ["A", "B", "C", "D", "E", "F", "G"]

def get_player_move(board):
    while True:
        col_letter = input("\nChoose a column (A–G): ").strip().upper()

        if col_letter not in possibleLetters:
            print("Invalid column.")
            continue

        col = possibleLetters.index(col_letter)

        if board.placePiece(col, "") is None and board.board[0][col] != "":
            print("Column is full.")
            continue

        return col
