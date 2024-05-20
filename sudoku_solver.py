class SudokuSolver:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def print_grid(self):
        for i in range(9):
            for j in range(9):
                print(self.grid[i][j], end=" ")
            print()

    def find_empty_location(self, l):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    l[0] = row
                    l[1] = col
                    return True
        return False

    def used_in_row(self, row, num):
        for i in range(9):
            if self.grid[row][i] == num:
                return True
        return False

    def used_in_col(self, col, num):
        for i in range(9):
            if self.grid[i][col] == num:
                return True
        return False

    def used_in_box(self, row, col, num):
        for i in range(3):
            for j in range(3):
                if self.grid[i + row][j + col] == num:
                    return True
        return False

    def check_location_is_safe(self, row, col, num):
        return not self.used_in_row(row, num) and (
            not self.used_in_col(col, num)
            and (not self.used_in_box(row - row % 3, col - col % 3, num))
        )

    def solve_sudoku(self):
        l = [0, 0]
        if not self.find_empty_location(l):
            return True

        row = l[0]
        col = l[1]

        for num in range(1, 10):
            if self.check_location_is_safe(row, col, num):
                self.grid[row][col] = num

                if self.solve_sudoku():
                    return True

                self.grid[row][col] = 0

        return False


# test

solver = SudokuSolver()
solver.grid = [
    [3, 0, 6, 5, 0, 8, 4, 0, 0],
    [5, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 7, 0, 0, 0, 0, 3, 1],
    [0, 0, 3, 0, 0, 0, 1, 8, 0],
    [9, 0, 0, 8, 6, 3, 0, 0, 5],
    [0, 5, 0, 0, 9, 0, 6, 0, 0],
    [1, 3, 0, 0, 0, 0, 2, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 7, 4],
    [0, 0, 5, 2, 0, 6, 3, 0, 0],
]

if solver.solve_sudoku():
    solver.print_grid()
else:
    print("No solution exists")
