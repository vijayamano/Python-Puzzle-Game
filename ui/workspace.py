from kivy.uix.widget import Widget
from kivy.lang.builder import Builder

Builder.load_file("ui/kv/workspace.kv")


class WorkSpace(Widget):
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
