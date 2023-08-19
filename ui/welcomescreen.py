from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.animation import Animation
from ui.levelscreen import LevelScreen
from kivy.uix.image import Image


Builder.load_file("ui/kv/welcome_screen.kv")


class WelcomeScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_enter(self, *args, **kwargs):
        """
        fired when the screen is added.
        """
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
        self.manager.init_transition(self.next_screen)

    def next_screen(self):
        """
        Transition to the next screen
        This function is called after the first animation plays
        and before the second animation plays
        """
        self.manager.switch_to(LevelScreen())
