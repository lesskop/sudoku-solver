import time

import screenshot
import recognition
import sudoku


def main() -> None:
    full_image = screenshot.capture_full_screen()
    sudoku_bounds = screenshot.find_sudoku_bounds(full_image)

    sudoku_image = screenshot.crop_to_sudoku(full_image)

    recognized_sudoku = recognition.recognize_sudoku(sudoku_image)
    print('Recognized sudoku:')
    sudoku.print_pretty(recognized_sudoku)

    solved_sudoku = sudoku.get_solution(recognized_sudoku)
    print('\nSolved sudoku:')
    sudoku.print_pretty(solved_sudoku)

    sudoku.fill_in_gui(solved_sudoku, sudoku_bounds)


if __name__ == '__main__':
    start = time.perf_counter()

    main()

    end = time.perf_counter()
    print(f'Time taken: {round(end - start, 2)} seconds')
