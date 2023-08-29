# Windows believes that kivy is DPI unaware, casuing scaling issues.
# The below code is needed to fix this issue
from ctypes import windll

windll.user32.SetProcessDpiAwarenessContext(-4)
from kivy.config import Config

Config.set("graphics", "width", "1280")
Config.set("graphics", "height", "720")
from PuzzleGame import PuzzleGame

if __name__ == "__main__":
    game = PuzzleGame()
    game.run()
