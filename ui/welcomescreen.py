from configparser import Interpolation
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.animation import Animation


Builder.load_string(
    """

<WelcomeScreen>:
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            source: "assets/textures/start_bg.png"

    Button:
        id: start_button
        pos_hint: {"center_x": 0.5, "center_y": 0}
        background_normal: "assets/textures/play_action_normal.png"
        background_down: "assets/textures/play_action_normal.png"
        size_hint: (0.3, 0.13) if self.state == "normal" else (0.29, 0.12)
        border: 10, 10, 10, 10
        canvas.before:
            Color:
                rgba: 0, 0, 0, 0.85
            BoxShadow:
                pos: self.pos
                size: self.size
                offset: 0, -5
                spread_radius: -10, -10
                border_radius: 10, 10, 10, 10
                blur_radius: 40 if self.state == "normal" else 20

    Button:
        id: help_button
        pos_hint: {"center_x": 0.1, "center_y": 0.2}
        background_normal: "assets/textures/help_action_normal.png"
        background_down: "assets/textures/help_action_normal.png"
        size_hint: None, None
        size: (100,100) if self.state == "normal" else (90,90)
        border: 10, 10, 10, 10
        canvas.before:
            Color:
                rgba: 0, 0, 0, 0.5
            BoxShadow:
                pos: self.pos
                size: self.size
                offset: 0, -3
                spread_radius: -3, -3
                border_radius: self.width / 2, self.width / 2, self.width / 2, self.width / 2
                blur_radius: 40 if self.state == "normal" else 10

    Image:
        id:title
        pos_hint: {"center_x": 0.5, "center_y": 1}
        source: "assets/textures/title_card.png"
        size: 0,0



"""
)


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
