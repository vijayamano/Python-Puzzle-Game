from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.metrics import dp

Builder.load_file("ui/kv/workspace.kv")


class WorkSpace(AnchorLayout):
    """
    This class represents the main work area for the player that is building the intended
    pattern. This class is responsible for handling the drag and drop of the shapes and
    creating a pseudo grid for the player to place the shapes on.
    """

    bg_texture = None
    """
    The texture of the background of the workspace
    """

    def __init__(self, **kwargs):
        self.bg_texture = "assets/textures/workspace_bg.png"
        super().__init__(**kwargs)
