from kivy.uix.image import Image
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file("ui/kv/shapepicker.kv")


class ShapeButton(ButtonBehavior, Image):
    has_clay = False
    """
    Represents whether the shape button has clay inside it or not
    """

    shape = None
    """
    The shape that this button represents
    """

    def on_press(self):
        """
        called when the button is pressed. Checks if the player is currently carrying clay
        """
        # First check if we already have clay in the shape
        if self.has_clay:
            # we already have clay in the shape so we check if the player is carrying clay
            if self.parent.cursor_object.carrying_clay:
                # the player is carrying clay so we tell the user to empty the shape first
                self.parent.cursor_object.show_popup(
                    "Error", "There is already clay here"
                )
                return super().on_press()
            else:
                # the player is not carrying clay so we attach the clay to the cursor
                # we check to see if the clay is colored.
                print(self.parent.cursor_object.colored)
                if self.parent.cursor_object.colored:
                    # the clay is colored so we switch over to rendering the colored shape
                    self.parent.cursor_object.pickup_shape(self.shape, self.color)
                    # now remove the clay from the shape
                    self.has_clay = False
                    self.parent.has_clay = False
                    # set the active shape to none
                    self.parent.active_shape = None
                    # reset the tint of the image
                    self.color = [1, 1, 1, 1]
                    # set the source to the empty version of the shape
                    self.source = self.source.replace("filled", "normal")
                    return super().on_press()
                self.parent.cursor_object.carrying_clay = True
                self.parent.cursor_object.colored = False
                self.parent.cursor_object.show_texture()
                # now remove the clay from the shape
                self.has_clay = False
                self.parent.has_clay = False
                # set the active shape to none
                self.parent.active_shape = None
                # reset the tint of the image
                self.color = [1, 1, 1, 1]
                # set the source to the empty version of the shape
                self.source = self.source.replace("filled", "normal")
                return super().on_press()
        if self.parent.cursor_object.carrying_clay:
            # now we check if there is already any other clay in the shape picker
            if self.parent.has_clay:
                # there is already clay in the shape picker so we tell the user to empty it first
                self.parent.cursor_object.show_popup(
                    "Error", "There is already clay here"
                )
                return super().on_press()
            # they are carrying clay so switch to the filled version of the shapes
            self.source = self.source.replace("normal", "filled")
            self.has_clay = True
            self.parent.has_clay = True
            # we then set the active shape to this shape
            self.parent.active_shape = self
            # we then remove the clay from the cursor
            self.parent.cursor_object.carrying_clay = False
            self.parent.cursor_object.colored = False
            # we then set the cursor texture to the shape that the player selected
            self.parent.cursor_object.remove_texture()

        else:
            # they are not carrying clay so tell the user to pick up clay first
            self.parent.cursor_object.show_popup(
                "Error", "Click on the clay jar first to pickup clay"
            )
        return super().on_press()

    pass


class ShapePicker(BoxLayout):
    cursor_object = None
    """
    A reference to the cursor object. This is needed to check if the player currently has
    clay selected or not.
    """

    bg_texture = None
    """
    Used to represent the background texture of the shape picker
    """

    has_clay = False
    """
    Represents whether the shape picker has clay inside it or not
    """

    active_shape = None
    """
    Stores a reference to the shape that currently has clay inside it
    """

    def __init__(self, **kw):
        self.bg_texture = Image(source="assets/textures/shape_picker_bg.png").texture
        super().__init__(**kw)
