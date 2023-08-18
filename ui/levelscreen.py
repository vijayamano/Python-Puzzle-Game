from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder


Builder.load_string(
    """
<LevelScreen>:
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            source: "assets/textures/start_bg.png"        

"""
)


class LevelScreen(Screen):
    """
    This is the screen that shows the level select screen.
    """

    def __init__(self, *args, **Kwargs):
        super().__init__(*args, **Kwargs)

    def on_start():
        pass
