from paddleocr import PaddleOCR
import pyautogui

# Delay in seconds between making moves and filling Sudoku cells. The default in PyAutoGUI 0.1 is too slow.
pyautogui.PAUSE = 0.02

# Delay in seconds before taking a screenshot
SCREENSHOT_DELAY = 1

# Create PaddleOCR instance for English language and GPU usage
OCR = PaddleOCR(lang='en', use_gpu=True)
