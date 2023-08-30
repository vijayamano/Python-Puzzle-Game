from kivy.uix.popup import Popup
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout

from ui.cursorshape import CursorShape

Builder.load_file("ui/kv/popupbase.kv")
Builder.load_file("ui/kv/cursorobject.kv")


class PopupBase(Popup):
    """
    Base class used to represent a popup. This class is used repeadetly to
    construct custom popups for various error messages within the game.
    """


class PopupContent(AnchorLayout):
    """
    This class is used to represent the content of the popup. This is used
    to display the content of the popup in a more organized manner.
    """

    description = None
    """
    The description of the popup
    """

    def __init__(self, description, **kwargs):
        self.description = description
        super().__init__(**kwargs)


class CursorObject(AnchorLayout):
    """
    This class is used to represent the cursor and any
    object that is being dragged along with it
    """

    carrying_clay = False
    """
    Represents whether the cursor is carrying clay or not.
    """

    colored = False
    """
    Is the carried clay colored or not.
    """

    should_display_texture = False
    """
    Boolean value that represents if we hsould 
    """

    carrying_shape = False
    """
    Represents whether the cursor is carrying a fully colored and shaped object
    """

    shape = None
    """
    Used to hold a reference to the object of the shape that is being carried
    """

    def __init__(self, **kwargs):
        # bind a function to the cursor position
        Window.bind(mouse_pos=self.on_mouse_pos)
        super().__init__(**kwargs)
        self.shape = self.ids.clay_cursor_shape
        self.ids.clay_cursor_image.opacity = 0
        self.shape.opacity = 0

    def on_mouse_pos(self, window, pos):
        """
        Called when the mouse moves
        """
        # check if we are carrying a shape
        if self.carrying_shape:
            # move the shape to the mouse position
            self.center = dp(pos[0]), dp(pos[1])
        # check if the cursor is carrying clay
        if self.carrying_clay:
            # move the cursor texture to the mouse position
            self.center = dp(pos[0]), dp(pos[1])

    def pickup_clay(self, amount):
        """
        Called when the player picks up clay from the claypot
        """
        # first we check if the player is carrying colored clay
        if self.carrying_shape:
            # this means that the player is currently carrying a shape
            # we cannot pick up clay while carrying a shape
            self.show_popup("Error", "You can only place colored clay on the workspace")
            return -1
        if self.colored:
            # this means the the player currently has some colored clay in a slot so they cant pick more
            self.show_popup("Error", "Clear the slot first to pick up more")
            return -1
        # the player is not carrying colored clay and we can continue
        # now check if the player is already carrying clay
        if self.carrying_clay:
            # we drop the clay back inside the pot
            self.carrying_clay = False
            self.colored = False
            # set the texture display to nothing
            self.remove_texture()
            return 0
        # now we check if there is enough clay to be picked up
        if amount <= 0:
            # there is no clay to be picked up
            self.show_popup("Woops!", "You ran out of Clay")
            return -1
        # the player is not carrying clay so we pick it up
        self.carrying_clay = True
        self.colored = False
        # display the clay on top of the mouse
        self.show_texture()
        return 1

    def pickup_shape(self, shape, color):
        """
        This function is called when the user picks up a shape
        """
        self.carrying_shape = True
        # create the new shape object and add it to the cursor
        self.shape = self.ids.clay_cursor_shape
        self.shape.opacity = 1
        self.shape.color = color
        self.shape.shape = shape
        # also bind to keyboard for rotation
        Window.bind(on_key_down=self.on_key_down)

    def drop_shape(self):
        """
        This function is called when the user drops a shape
        """
        self.carrying_shape = False
        # remove the shape from the cursor
        self.shape.opacity = 0
        self.shape.shape = ""
        self.colored = False
        self.carrying_clay = False
        # unbind the keyboard
        Window.unbind(on_key_down=self.on_key_down)

    def remove_texture(self):
        """
        Removes the texture from the cursor
        """
        self.ids.clay_cursor_image.opacity = 0
        self.should_display_texture = False

    def show_texture(self):
        """
        Shows the texture on the cursor
        """
        self.ids.clay_cursor_image.opacity = 1
        self.should_display_texture = True

    def show_popup(self, title, content):
        """
        Shows a popup when the player tries to drop colored clay
        back into the claypot
        """
        self.popup = PopupBase(title=title, content=PopupContent(description=content))
        self.popup.open()

    def on_key_down(self, window, key, *args):
        """
        Called when a key is pressed
        Is used to affect the rotation of the shape class
        """
        if key == 276:
            # the left arrow key was pressed
            self.shape.angle += 15
        elif key == 275:
            # the right arrow key was pressed
            self.shape.angle -= 15
