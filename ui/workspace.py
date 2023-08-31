from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang.builder import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scatter import Scatter
from kivy.graphics import Rectangle, Ellipse, Triangle, Color
from kivy.properties import NumericProperty
from kivy.uix.image import Image

Builder.load_file("ui/kv/workspace.kv")
Builder.load_file("ui/kv/displayshape.kv")


class DisplayShape(Scatter):
    """
    This class is used to represent a shape inside the work area
    """

    shape = "square"

    color = None

    angle = NumericProperty(0)

    def __init__(self, shape, color, angle):
        self.shape = shape
        self.color = color
        self.rotation = angle
        super().__init__()

    def on_kv_post(self, base_widget):
        self.add_shape()
        return super().on_kv_post(base_widget)

    def add_shape(self):
        self.ids.container.canvas.clear()
        self.ids.container.canvas.add(Color(rgba=self.color))
        if self.shape == "square":
            self.ids.container.canvas.add(Rectangle(size=(100, 100), pos=(0, 0)))
        elif self.shape == "circle":
            self.ids.container.canvas.add(Ellipse(size=(100, 100), pos=(0, 0)))
        elif self.shape == "triangle":
            self.ids.container.canvas.add(Triangle(points=[0, 0, 50, 87, 100, 0]))
        elif self.shape == "rhombus":
            image = Image(source="assets/textures/rhombus.png")
            self.canvas.add(
                Rectangle(texture=image.texture, size=image.texture_size, pos=(0, 0))
            )


class WorkSpace(ButtonBehavior, AnchorLayout):
    """
    This class represents the main work area for the player that is building the intended
    pattern. This class is responsible for handling the drag and drop of the shapes and
    creating a pseudo grid for the player to place the shapes on.
    """

    bg_texture = None
    """
    The texture of the background of the workspace
    """

    cursor_object = None
    """
    The cursor object that is being used to drag and drop the shapes
    """

    def __init__(self, **kwargs):
        self.bg_texture = "assets/textures/workspace_bg.png"
        super().__init__(**kwargs)

    def on_press(self):
        """
        This function is called when the player presses on the workspace
        """
        # check if the player is carrying a shape and not just normal clay
        if self.cursor_object.carrying_clay or not self.cursor_object.carrying_shape:
            self.cursor_object.show_popup(
                "Woops!", "You can only place colored clay on the workspace"
            )
            return
        # create a new cursor shape based on the shape that is being carried by the cursor
        new_shape = DisplayShape(
            shape=self.cursor_object.shape.shape,
            color=self.cursor_object.shape.color,
            angle=self.cursor_object.shape.angle,
        )
        new_shape.pos = self.ids.container.to_widget(*self.cursor_object.pos)
        self.cursor_object.drop_shape()
        self.ids.container.add_widget(new_shape)
