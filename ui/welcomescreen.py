from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.animation import Animation
from ui.levelscreen import LevelScreen
from kivy.uix.image import Image


Builder.load_file("ui/kv/welcome_screen.kv")


class WelcomeScreen(RelativeLayout):
    parent_screen = None
    """
    Stores a reference to this Screen's reference after its been added to the MainScreen.
    """

    bg_texture = None

    def __init__(self, *args, **kwargs):
        self.bg_texture = Image(
            source="assets/textures/start_bg.png", nocache=True
        ).texture
        self.bg_texture.wrap = "repeat"
        self.bg_texture.uvsize = (1, 1)
        super().__init__(*args, **kwargs)

    def on_start(self, *args, **kwargs):
        """
        fired when the screen is added.
        """
        self.parent_screen = self.parent
        # animate the title card
        Animation(
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            size=self.ids.title.texture.size,
            duration=0.5,
            t="in_out_circ",
        ).start(self.ids.title)
        Animation(
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            size_hint=(0.3, 0.13),
            duration=0.5,
            t="in_out_circ",
        ).start(self.ids.start_button)

    def on_start_click(self, widget):
        """
        Fired when the start button is clicked
        """
        self.parent_screen.transition(self.next_screen)

    def next_screen(self):
        """
        Transition to the next screen
        This function is called after the first animation plays
        and before the second animation plays
        """
        self.parent_screen.remove_widget(self)
        self.parent_screen.welcome_screen = None
        self.parent_screen.level_screen = LevelScreen()
        self.parent_screen.add_widget(self.parent_screen.level_screen, 0)
        self.parent_screen.level_screen.on_start()
