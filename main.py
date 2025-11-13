import random

print("Welcome to Connect Four")
print("-----------------------")

possibleLetters = ["A", "B", "C", "D", "E", "F", "G"]
rows = 6
cols = 7

# Create a 6x7 empty board
gameBoard = [["" for _ in range(cols)] for _ in range(rows)]


def printGameBoard():
    print("\n     A    B    C    D    E    F    G  ", end="")
    for x in range(rows):
        print("\n   +----+----+----+----+----+----+----+")
        print(x, " |", end="")
        for y in range(cols):
            cell = gameBoard[x][y]
            if cell in ("🔵", "🔴"):
                print("", cell, end=" |")
            else:
                print("   ", end=" |")
    print("\n   +----+----+----+----+----+----+----+")


def modifyArray(spacePicked, turn):
    gameBoard[spacePicked[0]][spacePicked[1]] = turn


def checkForWinner(chip):
    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(gameBoard[r][c + i] == chip for i in range(4)):
                print(f"\nGame over! {chip} wins! Thank you for playing :)")
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(gameBoard[r + i][c] == chip for i in range(4)):
                print(f"\nGame over! {chip} wins! Thank you for playing :)")
                return True

    # Diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(gameBoard[r + i][c + i] == chip for i in range(4)):
                print(f"\nGame over! {chip} wins! Thank you for playing :)")
                return True

    # Diagonal (down-left)
    for r in range(rows - 3):
        for c in range(3, cols):
            if all(gameBoard[r + i][c - i] == chip for i in range(4)):
                print(f"\nGame over! {chip} wins! Thank you for playing :)")
                return True

    return False


def findLowestAvailableRow(colIndex):
    """Return the lowest available row index for the given column, or None if full."""
    for r in range(rows - 1, -1, -1):
        if gameBoard[r][colIndex] == "":
            return r
    return None


def main():
    turnCounter = 0

    while True:
        printGameBoard()
        # --- Player turn ---
        if turnCounter % 2 == 0:
            while True:
                columnLetter = input("\nChoose a column (A–G): ").strip().upper()
                if columnLetter not in possibleLetters:
                    print("Invalid column. Try again.")
                    continue

                colIndex = possibleLetters.index(columnLetter)
                rowIndex = findLowestAvailableRow(colIndex)

                if rowIndex is None:
                    print("Column is full. Pick another one.")
                    continue

                modifyArray([rowIndex, colIndex], '🔵')
                break

            if checkForWinner('🔵'):
                printGameBoard()
                break

        # --- CPU turn ---
        else:
            while True:
                colIndex = random.randint(0, cols - 1)
                rowIndex = findLowestAvailableRow(colIndex)
                if rowIndex is not None:
                    modifyArray([rowIndex, colIndex], '🔴')
                    break

            if checkForWinner('🔴'):
                printGameBoard()
                break

        turnCounter += 1


if __name__ == "__main__":
    main()
