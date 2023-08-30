from kivy.uix.scatter import Scatter
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.graphics import Rectangle, Ellipse, Triangle, Color
from kivy.animation import Animation

Builder.load_file("ui/kv/cursorshape.kv")


class CursorShape(Scatter):
    """
    This class is used to represent a shape inside the work area
    """

    shape = StringProperty(None)
    """
    The shape that is being carried by the cursor
    """

    color = None
    """
    The color of the shape that is being carried by the cursor
    """

    angle = NumericProperty(0)
    """
    Represents the angle of the shape that is being carried by the cursor
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(shape=self.on_shape_change)

    def on_shape_change(self, instance, value):
        """ "
        This function is called when there is any change to the shape property.
        It is used to update the image of the shape.
        """
        # First clear the canvas of any shapes
        self.canvas.clear()
        # now add the color of the shape that has been selected to the instruction set
        self.canvas.add(Color(rgba=self.color))
        # now we set the canvas based on the type of shape
        if value == "square":
            # we are dealing with a rectangle so we draw a rectangle
            self.canvas.add(Rectangle(size=(100, 100), pos=(0, 0)))
        elif value == "circle":
            # we are dealing with a circle so we draw a circle
            self.canvas.add(Ellipse(size=(100, 100), pos=(0, 0)))
        elif value == "triangle":
            # we are dealing with a triangle so we draw a triangle
            self.canvas.add(Triangle(points=[0, 0, 50, 87, 100, 0]))
        elif value == "rhombus":
            # we are dealing with a rhombus so we draw a rhombus
            self.canvas.add(Triangle(points=[50, 0, 0, 50, 50, 100]))
            self.canvas.add(Triangle(points=[50, 0, 100, 50, 50, 100]))
