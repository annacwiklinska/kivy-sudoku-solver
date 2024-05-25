class SudokuSolver:
    def __init__(self, board):
        self.board = board

    def is_valid(self, row, col, num):
        # Check if the number is not in the given row
        for x in range(9):
            if self.board[row][x] == num:
                return False

        # Check if the number is not in the given column
        for x in range(9):
            if self.board[x][col] == num:
                return False

        # Check if the number is not in the 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False

        return True

    def is_initial_board_valid(self):
        # Check all cells for validity
        for row in range(9):
            for col in range(9):
                num = self.board[row][col]
                if num not in range(10):
                    return False
                if num != 0:
                    self.board[row][col] = 0  # Temporarily empty the cell
                    if not self.is_valid(row, col, num):
                        return False
                    self.board[row][col] = num  # Restore the cell
        return True

    def solve_sudoku(self):
        empty_spot = self.find_empty_location()
        if not empty_spot:
            return True  # No empty spot means the board is solved

        row, col = empty_spot

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve_sudoku():
                    return True
                self.board[row][col] = 0  # Undo the current cell for backtracking

        return False

    def find_empty_location(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) if num != 0 else "." for num in row))
