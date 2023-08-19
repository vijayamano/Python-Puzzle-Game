from kivy.lang.builder import Builder
from kivy.properties import (
    ObjectProperty,
    ListProperty,
    BooleanProperty,
    NumericProperty,
    StringProperty,
)
from kivy.uix.image import Image
from kivy.effects.scroll import ScrollEffect
from kivy.animation import Animation
from levels.levelhandler import LevelHandler
from ui.hoverbehaviour import HoverBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout


Builder.load_string(
    """
<LevelScreen>:
    name: "level_screen"
    
    RecycleView:
        viewclass: "LevelCard"
        id: recycle_view
        RecycleGridLayout:
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
                    texture: root.bg_texture
            default_size: None, dp(400)
            default_size_hint: 1, None
            padding: "80dp", "150dp", "80dp", "80dp"
            spacing: "80dp"
            size_hint_y: None
            height: self.minimum_height
            cols: 3

    Image:
        id: level_screen_title
        source: "assets/textures/level_screen_top.png"
        size_hint:None,None
        size:self.texture_size
        pos_hint:{'center_x':.5,'top':1}

    Button:
        id: back_button
        size_hint:None,None
        size:dp(75), dp(75)
        pos_hint:{'center_x':.1,'center_y':.9}
        background_normal:"assets/textures/back_button.png"
        background_down:"assets/textures/back_button.png"
        on_release:root.go_back()
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


    Button:
        id: settings_button
        size_hint:None,None
        size:dp(75), dp(75)
        pos_hint:{'center_x':.9,'center_y':.9}
        background_normal:"assets/textures/settings_button.png"
        background_down:"assets/textures/settings_button.png"
        on_release:root.show_settings()
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



                

<LevelCard>:
    height: self.width
    anchor_x: "center"
    anchor_y: "center"
    canvas.before:
        Color:
            rgba: 0, 0, 0, 0.6
        BoxShadow:
            pos: self.pos
            size: self.size
            offset: 0, -5
            spread_radius: -10, -10
            border_radius: 10, 10, 10, 10
            blur_radius: 40 if not self.hovering else 80
  
    Image:
        id:level_card_bg
        size_hint:1,1
        source: "assets/textures/level_card.png"
        fit_mode: "fill"

    BoxLayout:
        id: level_card_container
        size_hint: 1,1
        orientation: "vertical"
        padding: "30dp", "10dp", "30dp", "10dp"

        AnchorLayout:
            size_hint: 1,.7
            anchor_x: "center"
            anchor_y: "center"
            Image:
                id:level_card_preview_bg
                source: "assets/textures/level_preview_bg.png"
                size_hint: 1,1
                allow_stretch: True
            Image:
                id:level_card_preview
                source: root.preview_path
                size_hint: 1,1
                allow_stretch: True

        BoxLayout:
            id:level_card_info
            size_hint: 1,.3
            orientation:"horizontal"
            spacing: "10dp"

            Image:
                id:level_card_difficulty
                source: root.difficulty_image
                size_hint: .2,1
                allow_stretch: True

            AnchorLayout:
                size_hint: .8,1
                anchor_x: "center"
                anchor_y: "center"            
                Image:
                    id:level_card_title_bg
                    source: "assets/textures/level_title_bg.png"
                    size_hint: .8,1
                    fit_mode: "contain"

                Label:
                    id:level_card_title
                    text: "Level "+str(root.level_no)
                    font_size: "30dp"
                    color: 1,1,1,1
                    font_name: "assets/fonts/main.ttf"
"""
)


class LevelCard(AnchorLayout, HoverBehavior):
    """
    A class that represents a level card
    """

    hovering = BooleanProperty(False)
    """
    Represents whether the mouse is hovering over the widget
    """

    container_size = ListProperty([0, 0])
    """
    The size of the container
    """

    level_no = NumericProperty(0)
    """
    The level number
    """

    preview_path = StringProperty(None)
    """
    The path to the preview image
    """

    difficulty = StringProperty(None)
    """
    The difficulty of the level
    """

    difficulty_image = StringProperty(None)

    def on_enter(self, *args):
        """
        triggers when the mouse enters the widget
        """
        self.container_size = self.size
        self.hovering = True
        anim = Animation(size_hint=(1.05, 1.05), duration=0.2)
        anim.start(self.ids.level_card_bg)
        anim.start(self.ids.level_card_container)

    def on_leave(self, *args):
        """
        triggers when the mouse leaves the widget
        """
        anim = Animation(size_hint=(1, 1), duration=0.2)
        anim.bind(on_complete=self.set_false)
        anim.start(self.ids.level_card_bg)
        anim.start(self.ids.level_card_container)

    def set_false(self, *args):
        self.hovering = False


class LevelScreen(RelativeLayout):
    """
    This is the screen that shows the level select screen.
    """

    bg_texture = ObjectProperty(None)

    level_handler = LevelHandler()

    levels = []

    count = 0

    top_hidden = BooleanProperty(False)

    previous_y = NumericProperty(1)

    parent_screen = None

    def __init__(self, *args, **Kwargs):
        self.bg_texture = Image(
            source="assets/textures/start_bg.png", nocache=True
        ).texture
        self.bg_texture.uvsize = (1, 10)
        self.bg_texture.wrap = "repeat"
        super().__init__(*args, **Kwargs)
        # set the scroll effect
        self.ids.recycle_view.effect_cls = ScrollEffect
        # bind to the scroll of the recycele view
        self.ids.recycle_view.bind(scroll_y=self.on_scroll)
        # Load the level cards
        self.load_levels()

    def on_start(self):
        """
        This function triggers when the screen starts
        """
        self.parent_screen = self.parent

    def on_scroll(self, scroller, y):
        """
        This function triggers when the recyclerview scrolls.
        It is used to hide the top bar when the user scrolls down
        """
        if y < self.previous_y:
            if not self.top_hidden:
                self.top_hidden = True
                anim = Animation(pos_hint={"top": 1.2}, duration=1, t="in_out_circ")
                anim.start(self.ids.level_screen_title)
                anim1 = Animation(
                    pos_hint={"center_x": -0.1}, duration=1, t="in_out_circ"
                )
                anim1.start(self.ids.back_button)
                anim2 = Animation(
                    pos_hint={"center_x": 1.1}, duration=1, t="in_out_circ"
                )
                anim2.start(self.ids.settings_button)
        else:
            if self.top_hidden:
                self.top_hidden = False
                anim = Animation(pos_hint={"top": 1}, duration=1, t="in_out_circ")
                anim.start(self.ids.level_screen_title)
                anim1 = Animation(
                    pos_hint={"center_x": 0.1}, duration=1, t="in_out_circ"
                )
                anim1.start(self.ids.back_button)
                anim2 = Animation(
                    pos_hint={"center_x": 0.9}, duration=1, t="in_out_circ"
                )
                anim2.start(self.ids.settings_button)

        if (y - self.previous_y > 0.1) or (self.previous_y - y > 0.1):
            self.previous_y = round(y, 1)

    def go_back(self):
        """
        This function is used to go back to the main menu
        """
        self.parent_screen.transition(self.back_screen_setup)

    def back_screen_setup(self):
        from ui.welcomescreen import WelcomeScreen

        self.parent_screen.clear_widgets()
        self.parent_screen.level_screen = None
        self.parent_screen.welcome_screen = WelcomeScreen()
        self.parent_screen.add_widget(self.parent_screen.welcome_screen)
        self.parent_screen.welcome_screen.on_start()

    def show_settings(self):
        """
        This function is used to show the settings screen
        """
        print("showing settings")

    def load_levels(self):
        """ "
        Loads the levels from the level generator.
        """
        self.level_handler.load_levels()
        for level in (
            self.level_handler.easy_levels
            + self.level_handler.medium_levels
            + self.level_handler.hard_levels
        ):
            self.count += 1
            self.levels.append(
                {
                    "level_no": self.count,
                    "preview_path": level.preview_path,
                    "difficulty": level.difficulty,
                    "difficulty_image": level.difficulty_path,
                }
            )
        self.ids.recycle_view.data = self.levels
