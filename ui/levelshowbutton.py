from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang.builder import Builder
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file("ui/kv/levelshowbutton.kv")


class LevelShowButton(ButtonBehavior, AnchorLayout):
    """
    This class represents the button that is used to show the level.
    """
