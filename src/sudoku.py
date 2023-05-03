from typing import Optional, TypeAlias

import pyautogui

import screenshot

Sudoku: TypeAlias = list[list[int]]


def get_solution(sudoku: Sudoku) -> Sudoku:
    """
    Solves a Sudoku puzzle and returns the solution.

    :param sudoku: A `Sudoku` object, representing a list of lists, where each inner list represents
    a row of the Sudoku puzzle and contains the corresponding integers. If a cell is empty, its value is 0.
    :return: A `Sudoku` object, representing a solved Sudoku puzzle.
    """

    def find_empty_cell() -> Optional[tuple[int, int]]:
        """
        Finds the next empty cell (cell with 0 value) in the grid.

        :return: A tuple (row, col) representing the row and column of the next empty cell.
        If no empty cell is found, None is returned.
        """

        for row in range(9):
            for col in range(9):
                if sudoku[row][col] == 0:
                    return row, col
        return None

    def value_is_valid(row_idx: int, col_idx: int, val: int) -> bool:
        """
        Determines whether a given value can be placed in the given cell.

        :param row_idx: The row index of the cell.
        :param col_idx: The column index of the cell.
        :param val: The value to be placed in the cell.
        :return: True if the value can be placed in the cell without violating the Sudoku rules, False otherwise.
        """

        row_ok = all(val != sudoku[row_idx][k] for k in range(9))
        if row_ok:
            col_ok = all(val != sudoku[k][col_idx] for k in range(9))
            if col_ok:
                box_row, box_col = 3 * (row_idx // 3), 3 * (col_idx // 3)
                for box_row_idx in range(box_row, box_row + 3):
                    for box_col_idx in range(box_col, box_col + 3):
                        if val == sudoku[box_row_idx][box_col_idx]:
                            return False
                return True
        return False

    def backtrack() -> bool:
        """
        Backtracking algorithm for solving the Sudoku puzzle.

        :return: True if a solution was found, False otherwise.
        """

        empty_cell = find_empty_cell()
        if empty_cell is None:
            return True
        row, col = empty_cell
        for value in range(1, 10):
            if value_is_valid(row, col, value):
                sudoku[row][col] = value
                if backtrack():
                    return True
                sudoku[row][col] = 0
        return False

    backtrack()
    return sudoku


def print_pretty(sudoku: Sudoku) -> None:
    """
    Prints a Sudoku puzzle in a nicely formatted way.

    :param sudoku: A `Sudoku` object, representing a list of lists, where each inner list represents
    a row of the Sudoku puzzle and contains the corresponding integers.
    """

    horizontal_divider = '-------------------------'
    vertical_divider = '|'

    print(horizontal_divider)

    for i, row in enumerate(sudoku):
        print(vertical_divider, end=' ')

        for j, digit in enumerate(row):
            print(digit, end=' ')

            if (j + 1) % 3 == 0:
                print(vertical_divider, end=' ')

        print()

        if (i + 1) % 3 == 0 and i != 8:
            print(horizontal_divider)

    print(horizontal_divider)


def click_on_first_cell(bounds: screenshot.SudokuBounds) -> None:
    """
    Clicks the center of the top-left cell in the Sudoku puzzle area.

    :param bounds: A `SudokuBounds` object representing the boundaries of the Sudoku puzzle area on the screenshot.
    """

    cell_center_width = bounds.cell_width / 2
    cell_center_x = bounds.top_left_x + cell_center_width
    cell_center_y = bounds.top_left_y + cell_center_width
    pyautogui.click(cell_center_x, cell_center_y)


def fill_in_gui(sudoku: Sudoku, bounds: screenshot.SudokuBounds) -> None:
    """
    Fills in a Sudoku grid on sites like sudoku.com by imitating keystrokes on the keyboard.
    This works on Sudoku sites where you can use arrows to move around the cells and numbers to fill in.

    :param sudoku: A `Sudoku` object, representing a solved Sudoku puzzle.
    :param bounds: A `SudokuBounds` object representing the boundaries of the Sudoku puzzle area on the screenshot.
    """
    click_on_first_cell(bounds)

    for row in range(9):
        for i in range(9):
            pyautogui.press(str(sudoku[row][i]))
            pyautogui.press('right')
        for i in range(9):
            pyautogui.press('left')
        pyautogui.press('down')
