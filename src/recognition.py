from PIL import Image
import numpy as np

import screenshot
import config
import sudoku


def recognize_digit(cell_image: Image) -> int:
    """
    Recognizes and extracts a single digit from a cell image using PaddleOCR.

    :param cell_image: The input Sudoku cell image.
    :return: The recognized digit as an integer. If no digit is recognized, 0 is returned.
    """

    recognition_data = config.OCR.ocr(np.array(cell_image), det=False, rec=True, cls=False)
    digit = recognition_data[0][0][0] if recognition_data else ''

    if digit == '':
        return 0

    return int(digit)


def recognize_sudoku(img: Image) -> sudoku.Sudoku:
    """
    Recognizes and extracts the digits from a Sudoku puzzle image using PaddleOCR.

    :param img: A PIL object of the Sudoku image.
    :return: A `Sudoku` object, representing a list of lists, where each inner list represents
    a row of the Sudoku puzzle and contains the corresponding integers. If a cell is empty, its value is 0.
    """

    cell_width = img.size[0] // 9
    cells_coordinates = screenshot.get_sudoku_cells_coordinates(cell_width)

    digits = []
    for cell in cells_coordinates:
        cell_img = img.crop((cell.x0, cell.y0, cell.x1, cell.y1))
        digit = recognize_digit(cell_img)
        digits.append(digit)

    grid = []
    for i in range(0, len(digits), 9):
        grid.append(digits[i:i + 9])

    return grid
