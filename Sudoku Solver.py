# Section: Import modules

import pandas as pd

from os.path import dirname, abspath

from copy import copy

import time

# Section End

# Section: Constants

SUDOKUPATH = dirname(abspath(__file__)) + "\\Sudokus\\"

# Section End

# Section: Sudoku Solver class


class SudokuSolver():

    def __init__(self):
        self.sudokus = self.importSudokus()

    def solve(self):

        for sudoku in self.sudokus:
            self.solveSudoku(sudoku)

    def importSudokus(self):
        sudokus = []
        for sudokuName in ["easy", "intermediate", "hard", "expert"]:
            sudoku = self.importSudoku(sudokuName)
            if sudoku is not None:
                sudokus.append({"sudokuName": sudokuName, "sudokuMatrix": sudoku})

        return sudokus

    def importSudoku(self, sudokuName):
        sudoku = pd.read_csv(
            SUDOKUPATH + sudokuName.lower() + ".csv", header=None, dtype=pd.Int64Dtype()).fillna(0).values
        if self.checkValidity(sudoku):
            return sudoku
        return None

    def printSudoku(self, sudoku):
        rowCount = 0
        for row in sudoku:
            if rowCount % 3 == 0:
                print()
            columnCount = 0
            for cell in row:
                if columnCount % 3 == 0:
                    print("  ", end="")
                if cell == 0:
                    cell = "-"
                print(cell, end=" ")
                columnCount += 1
            rowCount += 1
            print()

    def checkValidity(self, sudoku):
        for rowIndex in range(len(sudoku)):
            if not self.checkRow(rowIndex, sudoku):
                return False

        for columnIndex in range(len(sudoku[0])):
            if not self.checkColumn(columnIndex, sudoku):
                return False

        for y in range(0, 3):
            for x in range(0, 3):
                if not self.checkSection((y, x), sudoku):
                    return False

        return True

    def checkRow(self, rowIndex, sudoku):
        return self.checkArray(sudoku[rowIndex])

    def checkColumn(self, columnIndex, sudoku):
        return self.checkArray(sudoku[:, columnIndex])

    def checkSection(self, section, sudoku):
        y, x = section
        y *= 3
        x *= 3
        subMatrix = sudoku[y: y+3, x: x+3]
        subArray = subMatrix.reshape(1, -1)[0]
        return self.checkArray(subArray)

    def checkCell(self, position, sudoku):
        rowIndex, columnIndex = position
        section = [rowIndex//3, columnIndex//3]
        if (self.checkRow(rowIndex, sudoku)
                and self.checkColumn(columnIndex, sudoku)
                and self.checkSection(section, sudoku)):
            return True
        return False

    def checkArray(self, array):
        # print(f"Checking Array: {array}")
        # Remove empties
        noEmptyArray = array[array != 0]

        # Remove duplicates and anything out of range
        newArray = set(noEmptyArray[(noEmptyArray > 0) & (noEmptyArray < 10)])

        if len(noEmptyArray) == len(newArray):
            return True
        return False

    def solveSudoku(self, sudoku):
        sudokuName = sudoku["sudokuName"]
        sudokuMatrix = sudoku["sudokuMatrix"]
        print(sudokuName.upper())
        self.printSudoku(sudokuMatrix)
        print()
        print("Solving...")
        startTime = time.time()
        solvedSudoku = self.backtrack(sudokuMatrix)
        self.printSudoku(solvedSudoku)
        endTime = time.time()
        secondsElapsed = endTime - startTime
        print(f"Solved in {secondsElapsed:.3f} seconds")
        print("\n")

    def backtrack(self, sudoku, position=(0, 0), indent=""):
        # print(f"\n{indent}Looking at cell {position} in")
        #for row in sudoku:
        #    print(f"{indent}{row}")
        # Base Case
        if 9 in position:
            # print(f"{indent}Base Case")
            return sudoku

        # Recursive Case
        else:
            cell = sudoku[position]
            y, x = position
            newPosition = ((y + ((x + 1) // 9)), (x + 1) % 9)
            indent += "  "

            # If cell is filled
            if cell != 0:
                result = self.backtrack(sudoku, newPosition, indent)
                if result is not False:
                    return result
            # If cell is unfilled
            else:
                for possibleNum in range(1, 10):
                    # print(f"{indent}Trying {possibleNum}")
                    potentialSudoku = sudoku.copy()
                    potentialSudoku[y, x] = possibleNum
                    if self.checkCell(position, potentialSudoku):
                        result = self.backtrack(potentialSudoku, newPosition, indent)
                        if result is not False:
                            return result
            return False


# Section End

# Section: Main function


def main():
    SS = SudokuSolver()
    SS.solve()


if __name__ == "__main__":
    main()

# Section End
