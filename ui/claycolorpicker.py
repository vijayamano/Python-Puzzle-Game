from kivy.uix.gridlayout import GridLayout
from kivy.lang.builder import Builder
from kivy.uix.image import Image

Builder.load_file("ui/kv/colorpicker.kv")


class ClayColorPicker(GridLayout):
    """
    This class is used to represent the color picker
    """

    bg_texture = None
    """
    The texture of the background of the color picker
    """

    def __init__(self, **kwargs):
        self.bg_texture = Image(source="assets/textures/color_picker_bg.png")
        super().__init__(**kwargs)
