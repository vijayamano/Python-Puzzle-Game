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
from kivy.uix.modalview import ModalView


Builder.load_file("ui/kv/levelscreen.kv")
Builder.load_file("ui/kv/levelcard.kv")


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

    level_no = StringProperty()
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


class DifficultyMenu(ModalView):
    pass


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
        # add the inifinite level card as the first card in the list
        self.levels.append(
            {
                "level_no": "Endless",
                "preview_path": "assets/textures/infinite_preview.png",
                "difficulty": "∞",
                "difficulty_image": "assets/textures/infinite.png",
            }
        )
        for level in (
            self.level_handler.easy_levels
            + self.level_handler.medium_levels
            + self.level_handler.hard_levels
        ):
            self.count += 1
            self.levels.append(
                {
                    "level_no": "Level " + str(self.count),
                    "preview_path": level.preview_path,
                    "difficulty": level.difficulty,
                    "difficulty_image": level.difficulty_path,
                }
            )
        self.ids.recycle_view.data = self.levels

    def show_difficulty(self):
        """
        Opens up a modal dialogue for picking difficulty
        """
