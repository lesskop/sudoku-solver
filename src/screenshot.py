from typing import TypeAlias
from dataclasses import dataclass
import time

from PIL import Image, ImageGrab
import numpy as np
import cv2

import config

Pixels: TypeAlias = int


@dataclass(frozen=True)
class SudokuBounds:
    top_left_x: Pixels
    top_left_y: Pixels
    width: Pixels
    cell_width: Pixels


@dataclass(frozen=True)
class CellCoordinates:
    x0: Pixels
    y0: Pixels
    x1: Pixels
    y1: Pixels


def capture_full_screen() -> Image:
    """
    Captures the full screen with a delay and returns a PIL Image object.

    :return: A PIL Image object representing the full screen.
    """

    time.sleep(config.SCREENSHOT_DELAY)
    return ImageGrab.grab()


def find_sudoku_bounds(screenshot: Image) -> SudokuBounds:
    """
    Finds Sudoku bounds in the screenshot using computer vision algorithms.

    :param screenshot: A PIL Image object representing the screenshot of the entire screen.
    :return: A `SudokuBounds` object representing the boundaries of the Sudoku puzzle area on the screenshot.
    """
    gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    edges = cv2.Canny(thresh, 50, 100)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    top_left_x = 0
    top_left_y = 0
    square_width = 0
    square_threshold = 0.005

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.005 * perimeter, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = abs(w - h) / min(w, h)
            if aspect_ratio < square_threshold and w > square_width:
                roi = thresh[y:y+h, x:x+w]
                lines = cv2.HoughLinesP(roi, rho=1, theta=np.pi/180, threshold=50, minLineLength=w//2, maxLineGap=w//10)
                if lines is not None and len(lines) >= 16:
                    top_left_x, top_left_y, square_width = x, y, w

    return SudokuBounds(top_left_x, top_left_y, square_width, square_width // 9)


def crop_to_sudoku(screenshot: Image) -> Image:
    """
    Crops the screenshot to Sudoku, converts the image to black and white and returns it.

    :param screenshot: A PIL Image object representing the screenshot of the entire screen.
    :return: A PIL Image object representing a Sudoku puzzle.
    """

    sudoku_bounds = find_sudoku_bounds(screenshot)
    y, x, image_width = sudoku_bounds.top_left_y, sudoku_bounds.top_left_x, sudoku_bounds.width
    cropped_image = np.array(screenshot)[y:y + image_width, x:x + image_width]

    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return Image.fromarray(thresh)


def get_sudoku_cells_coordinates(cell_width: Pixels) -> list[CellCoordinates]:
    """
    Returns a list of the cell coordinates on the Sudoku image, not on a full screenshot.

    :param cell_width: Width of the Sudoku cell in pixels.
    :return: A list of `CellCoordinates` objects, each representing the (x0, y0) coordinates
    of the top-left corner of a cell and the (x1, y1) coordinates of its bottom-right corner.
    """

    border_offset: Pixels = 5
    cells = []

    for row in range(9):
        for col in range(9):
            x0 = col * cell_width + border_offset
            y0 = row * cell_width + border_offset
            x1 = x0 + cell_width - border_offset
            y1 = y0 + cell_width - border_offset
            cells.append(CellCoordinates(x0, y0, x1, y1))

    return cells
