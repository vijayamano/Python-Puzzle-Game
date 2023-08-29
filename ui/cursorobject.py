from re import I
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout

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


class CursorObject(Image):
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

    def __init__(self, **kwargs):
        # bind a function to the cursor position
        Window.bind(mouse_pos=self.on_mouse_pos)
        super().__init__(**kwargs)
        self.opacity = 0

    def on_mouse_pos(self, window, pos):
        """
        Called when the mouse moves
        """
        # check if the cursor is carrying clay
        if self.carrying_clay:
            # move the cursor texture to the mouse position
            self.center = dp(pos[0]), dp(pos[1])

    def pickup_clay(self):
        """
        Called when the player picks up clay from the claypot
        """
        # first we check if the player is carrying colored clay
        if self.carrying_clay and self.colored:
            # this means that the player currently has a colored clay
            # we cannot drop colored clay back in so show popup
            self.show_popup("Error", "You cannot drop colored clay back in the claypot")
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
        # the player is not carrying clay so we pick it up
        self.carrying_clay = True
        self.colored = False
        # display the clay on top of the mouse
        self.show_texture()
        return 1

    def remove_texture(self):
        """
        Removes the texture from the cursor
        """
        self.source = ""
        self.opacity = 0
        self.should_display_texture = False

    def show_texture(self):
        """
        Shows the texture on the cursor
        """
        self.source = "assets/textures/clay_cursor.png"
        self.opacity = 1
        self.should_display_texture = True

    def show_popup(self, title, content):
        """
        Shows a popup when the player tries to drop colored clay
        back into the claypot
        """
        self.popup = PopupBase(title=title, content=PopupContent(description=content))
        self.popup.open()
