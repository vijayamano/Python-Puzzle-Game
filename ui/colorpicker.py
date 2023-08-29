from kivy.uix.gridlayout import GridLayout
from kivy.lang.builder import Builder
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


Builder.load_file("ui/kv/claycolorpicker.kv")


class ColorButton(ButtonBehavior, Image):
    tint_color = None
    """
    The tint color of the color button.
    Not used in displaying but used to assign color to the clay object
    """

    def on_release(self, **kwargs):
        """
        Called on release of the color button. This function will assign color to our clay object
        """
        # first we check if there is clay inside the shape picker
        if self.parent.shape_picker.has_clay:
            # there is clay inside the shape picker so we can color it
            self.parent.shape_picker.active_shape.color = self.tint_color
            self.parent.cursor_object.colored = True
        else:
            # there is no clay inside the shape picker so we tell the user to pick up clay first
            self.parent.shape_picker.cursor_object.show_popup(
                "Error", "No clay to color"
            )


class ClayColorPicker(GridLayout):
    """
    This class is used to represent the color picker
    """

    bg_texture = None
    """
    The texture of the background of the color picker
    """

    cursor_object = None
    """
    Used to maintain a reference to the cursor object
    """

    shape_picker = None
    """
    Used to maintain reference to the shape picker object
    """

    def __init__(self, **kwargs):
        self.bg_texture = Image(source="assets/textures/color_picker_bg.png").texture
        super().__init__(**kwargs)
