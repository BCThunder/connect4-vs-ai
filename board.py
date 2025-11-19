rows = 6
cols = 7

class Connect4Board:
    def __init__(self):
        self.board = [["" for _ in range(cols)] for _ in range(rows)]

    def printBoard(self):
        print("\n     A    B    C    D    E    F    G")
        for x in range(rows):
            print("   +----+----+----+----+----+----+----+")
            print(f" {x} |", end="")
            for y in range(cols):
                cell = self.board[x][y]
                # Always print a 3-width cell
                if cell in ("🔵", "🔴"):
                    print(f" {cell} ", end="|")
                else:
                    print("    ", end="|")
            print()  # end row
        print("   +----+----+----+----+----+----+----+")


    def placePiece(self, col, chip):
        """Places a chip in a column, returns (row, col) or None if full."""
        for r in range(rows - 1, -1, -1):
            if self.board[r][col] == "":
                self.board[r][col] = chip
                return (r, col)
        return None

    def getValidMoves(self):
        return [c for c in range(cols) if self.board[0][c] == ""]

    def checkWin(self, chip):
        # Horizontal
        for r in range(rows):
            for c in range(cols - 3):
                if all(self.board[r][c + i] == chip for i in range(4)):
                    return True

        # Vertical
        for c in range(cols):
            for r in range(rows - 3):
                if all(self.board[r + i][c] == chip for i in range(4)):
                    return True

        # Down-right diagonal
        for r in range(rows - 3):
            for c in range(cols - 3):
                if all(self.board[r + i][c + i] == chip for i in range(4)):
                    return True

        # Down-left diagonal
        for r in range(rows - 3):
            for c in range(3, cols):
                if all(self.board[r + i][c - i] == chip for i in range(4)):
                    return True

        return False

    def clone(self):
        new_b = Connect4Board()
        new_b.board = [row[:] for row in self.board]
        return new_b
