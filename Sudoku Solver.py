# Section: Import modules

import pandas as pd

import numpy as np

from os.path import dirname, abspath

# Section End

# Section: Constants

SUDOKUPATH = dirname(abspath(__file__)) + "\\Sudokus\\"

# Section End

# Section: Sudoku Solver class


class SudokuSolver():

    def __init__(self):
        sudokus = self.importSudokus()

        for sudoku in sudokus:
            self.solveSudoku(sudoku)

    def importSudokus(self):
        sudokus = []
        for sudokuName in ["easy"]:  # , "intermediate", "hard", "expert"]:
            sudoku = self.importSudoku(sudokuName)
            if sudoku is not None:
                sudokus.append(sudoku)

        return sudokus

    def importSudoku(self, sudokuName):
        sudoku = pd.read_csv(
            SUDOKUPATH + sudokuName.lower() + ".csv", header=None, dtype=int).values

        if self.checkValidity(sudoku):
            return sudoku
        return None

    def checkValidity(self, sudoku):
        for row in sudoku:
            if not self.checkArray(row):
                return False

        for column in sudoku.T:
            if not self.checkArray(column):
                return False

        for yTrisector in range(0, 3):
            y = yTrisector * 3
            for xTrisector in range(0, 3):
                x = xTrisector * 3
                subMatrix = sudoku[y: y+3, x: x+3]
                subArray = subMatrix.reshape(1, -1)[0]
                if not self.checkArray(subArray):
                    return False

        return True

    def checkArray(self, array):
        # Remove empties
        noEmptyArray = array[array != 0]

        # Remove duplicates and anything out of range
        newArray = set(noEmptyArray[(noEmptyArray > 0) & (noEmptyArray < 10)])

        if len(noEmptyArray) == len(newArray):
            return True
        return False

    def solveSudoku(self, sudoku):
        print(sudoku)


# Section End

# Section: Main function


def main():
    SS = SudokuSolver()


if __name__ == "__main__":
    main()

# Section End
