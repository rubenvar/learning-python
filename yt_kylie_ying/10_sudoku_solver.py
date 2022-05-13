def find_next_empty(puzzle):
    # find the next col, row that's not filled
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c

    return None, None


def is_valid(puzzle, guess, row, col):
    # check if the guess is valid (True) for that row and column

    # check in row
    row_vals = puzzle[row]
    if guess in row_vals:
        return False

    # check in column
    # col_vals = []
    # for i in range(9):
    #     col_vals.append(puzzle[i][col])
    # equals this ⬆
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    # check in box (this is tricky)
    # get where the 3x3 box starts for the given location
    row_start = (row // 3) * 3  # 1 // 3 = 0, 5 // 3 = 1, etc.
    col_start = (col // 3) * 3
    # and iterate over the values inside the box
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False

    # valid guess
    return True


def solve_sudoku(puzzle):
    # solve sudoku by backtracking
    # puzzle is a list of lists, each list is a row
    # return if there is solution
    # mutate the puzzle to be the solution

    # 1. choose somewhere to make a guess
    row, col = find_next_empty(puzzle)

    # if nowhere left, then we're done
    if row is None:
        return True

    # 2. if free place to put the guess, make a guess between 1 and 9
    for guess in range(1, 10):
        # 3. check if valid guess
        if is_valid(puzzle, guess, row, col):
            # 3.1 place the guess in the puzzle
            puzzle[row][col] = guess
            # 4. recurse
            if solve_sudoku(puzzle):
                return True

        # 5. if not valid OR the guess doesn't solve:
        # backtrack
        puzzle[row][col] = -1  # reset

    # if nothing works... unsolvable
    return False


if __name__ == '__main__':
    example_board = [
        [3, 9, -1, -1, 5, -1, -1, -1, -1],
        [-1, -1, -1, 2, -1, -1, -1, -1, 5],
        [-1, -1, -1, 7, 1, 9, -1, 8, -1],
        [-1, 5, -1, -1, 6, 8, -1, -1, -1],
        [2, -1, 6, -1, -1, 3, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, 4],
        [5, -1, -1, -1, -1, -1, -1, -1, -1],
        [6, 7, -1, 1, -1, 5, -1, 4, -1],
        [1, -1, 9, -1, -1, -1, 2, -1, -1]
    ]
    print(solve_sudoku(example_board))
    print(example_board)
