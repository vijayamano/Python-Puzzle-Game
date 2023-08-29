from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from ui.cursorobject import CursorObject
from ui.shapepicker import ShapePicker
from ui.colorpicker import ClayColorPicker
from kivy.animation import Animation

Builder.load_file("ui/kv/gamescreen.kv")
Builder.load_file("ui/kv/clayjar.kv")


class ClayJar(ButtonBehavior, RelativeLayout):
    """
    This class is used to represent the clay jar. It controls the amount of
    clay inside the pot, if there is any more clay inside the pot. These
    parameters can be set and tweaked based on the level difficulty
    """

    max_clay_amount = None
    """
    The maximum amount of clay that can be stored in the jar
    """

    current_clay_amount = None
    """
    The current amount of clay that is stored in the jar
    """

    object_texture = None
    """
    The texture of the Clay Jar
    """

    cursor_object = None
    """
    Represents the cursor and details of the object that is being dragged with it
    """

    def __init__(self, *args, **kwargs):
        self.object_texture = Image(
            source="assets/textures/clay_jar.png", nocache=True
        ).texture
        super().__init__(*args, **kwargs)

    def on_press(self):
        """
        This function is called when the clay jar is pressed. Animates the jar
        to grow bigger in size slightly"
        """
        Animation(size_hint=(0.12, 0.22), duration=0.1).start(self)
        return super().on_press()

    def on_release(self):
        """
        This function is called when the clay jar is released. Animates the jar
        to shrink back to its original size. It also determines whether it is
        possible to take clay from the jar or not.
        """
        Animation(size_hint=(0.1, 0.2), duration=0.1).start(self)
        match self.cursor_object.pickup_clay():
            case 0:
                # we dropped the clay
                print("dropped clay")
                self.current_clay_amount += 1

            case 1:
                # we picked up the clay
                print("picked up clay")
                self.current_clay_amount -= 1

        return super().on_release()


class GameScreen(Screen):
    """
    This class is used to represent the main game screen
    """

    bg_texture = None
    """
    The image texture that is used for the background of this screen
    """

    cursor_object = None
    """
    Represents the cursor and details about the object that is being dragged with it
    """

    def __init__(self, *args, **kwargs):
        self.bg_texture = Image(
            source="assets/textures/start_bg.png", nocache=True
        ).texture
        self.bg_texture.uvsize = (1, 2)
        self.bg_texture.wrap = "repeat"
        self.name = "game_screen"
        super().__init__(*args, **kwargs)
        # create a cursor object and add it to screen
        self.cursor_object = CursorObject()
        self.add_widget(self.cursor_object)
        # set the clay jar's cursor picker
        self.ids.clay_jar.cursor_object = self.cursor_object
        self.ids.clay_jar.current_clay_amount = 10
        # set the shape picker cursor object
        self.ids.shape_picker.cursor_object = self.cursor_object
        # set the color picker cursor object
        self.ids.color_picker.cursor_object = self.cursor_object
        # set the shape picker reference of the color picker
        self.ids.color_picker.shape_picker = self.ids.shape_picker

    def on_enter(self, *aargs, **kwargs):
        print("hello")
