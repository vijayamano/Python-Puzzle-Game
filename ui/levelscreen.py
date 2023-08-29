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
from levels.LevelHandler import LevelHandler
from ui.GameScreen import GameScreen
from ui.hoverbehaviour import HoverBehavior
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.effectwidget import EffectWidget

Builder.load_file("ui/kv/levelscreen.kv")
Builder.load_file("ui/kv/levelcard.kv")
Builder.load_file("ui/kv/difficulty_menu.kv")


class DifficultyMenu(ModalView):
    parent_screen = ObjectProperty(None)
    """
    Stores the parent screen
    """

    closing = False

    def on_dismiss(self):
        """
        This function triggers when the modal view is dismissed.
        It is used to animate the blur effect back to normal
        """
        Animation(blur_amount=0, duration=0.3).start(self.parent_screen)
        if not self.closing:
            anim = Animation(opacity=0, duration=0.3)
            anim.bind(on_complete=self.close)
            anim.start(self)
            self.closing = True
            return True
        else:
            return super().on_dismiss()

    def close(self, *args):
        self.dismiss()

    def on_open(self):
        """
        This function triggers when the modal view is opened.
        It is used to animate all the widgets into place
        """
        # aniamte the opacity of the popup
        Animation(opacity=1, size_hint=(0.6, 0.8), duration=0.5, t="out_back").start(
            self
        )
        # aniamte the size of the three buttons
        anim = Animation(size_hint=(0.6, 0.2), duration=0.5, t="out_back")
        anim.start(self.ids.easy_button)
        anim.start(self.ids.medium_button)
        anim.start(self.ids.hard_button)
        return super().on_open()


class DifficultyButton(ButtonBehavior, Image, HoverBehavior):
    """
    This class represents the difficulty buttons that appear
    when selecting endless mode. They where created as a seperate
    class due to the requirement of the hover effect
    """

    hovering = BooleanProperty(False)

    def on_enter(self, *args):
        """
        triggers when the mouse enters the widget.
        Used to raise the widget
        """
        self.hovering = True
        Animation(size_hint=(0.63, 0.22), duration=0.2).start(self)

    def on_leave(self, *args):
        """
        triggers when the mouse leaves the widget.
        Used to lower the widget
        """
        anim = Animation(size_hint=(0.6, 0.2), duration=0.2)
        anim.bind(on_complete=self.set_false)
        anim.start(self)

    def set_false(self, *args):
        self.hovering = False


class LevelCard(ButtonBehavior, AnchorLayout, HoverBehavior):
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
    """
    The path to the difficulty image
    """

    parent_container = ObjectProperty(None)
    """
    The parent container of the level card
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_enter(self, *args):
        """
        triggers when the mouse enters the widget
        """
        self.container_size = self.size
        self.hovering = True
        anim = Animation(size_hint=(1.05, 1.05), duration=0.2)
        anim.start(self.ids.level_card_bg)
        anim.start(self.ids.level_card_container)

    def on_press(self):
        """
        triggers when the widget is pressed
        """
        if self.level_no == "Endless":
            self.parent_container.show_difficulty()
        else:
            self.parent_container.select_level()

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


class LevelScreen(EffectWidget, Screen):
    """
    This is the screen that shows the level select screen.
    """

    bg_texture = None
    """
    The texture of the background
    """

    level_handler = None
    """
    The level handler object
    """

    count = 0
    """
    internal variable used to keep count of the number of levels
    """

    top_hidden = BooleanProperty(False)
    """
    Represents whether the top bar is hidden
    """

    previous_y = NumericProperty(1)
    """
    Stores the previous y value of the scroll
    """

    blur_amount = NumericProperty(0.0)
    """
    used to animate the blur affect when showing difficulty menu
    """

    def __init__(self, *args, **Kwargs):
        self.bg_texture = Image(
            source="assets/textures/level_bg.png", nocache=True
        ).texture
        self.bg_texture.uvsize = (1, 20)
        self.bg_texture.wrap = "repeat"
        super().__init__(*args, **Kwargs)
        # set the scroll effect
        self.ids.recycle_view.effect_cls = ScrollEffect
        # bind to the scroll of the recycele view
        self.ids.recycle_view.bind(scroll_y=self.on_scroll)
        # Load the level cards
        self.load_levels()

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
        self.manager.init_transition(self.back_screen_setup)

    def back_screen_setup(self):
        from ui.welcomescreen import WelcomeScreen

        self.manager.switch_to(WelcomeScreen())

    def show_settings(self):
        """
        This function is used to show the settings screen
        """
        print("showing settings")

    def load_levels(self):
        """ "
        Loads the levels from the level generator.
        """
        self.level_handler = LevelHandler()
        self.level_handler.load_levels()
        # add the inifinite level card as the first card in the list
        levels = []
        levels.append(
            {
                "level_no": "Endless",
                "preview_path": "assets/textures/infinite_preview.png",
                "difficulty": "∞",
                "difficulty_image": "assets/textures/infinite.png",
                "parent_container": self,
            }
        )
        for level in (
            self.level_handler.easy_levels
            + self.level_handler.medium_levels
            + self.level_handler.hard_levels
        ):
            self.count += 1
            levels.append(
                {
                    "level_no": "Level " + str(self.count),
                    "preview_path": level.preview_path,
                    "difficulty": level.difficulty,
                    "difficulty_image": level.difficulty_path,
                    "parent_container": self,
                }
            )
        self.ids.recycle_view.data = levels

    def show_difficulty(self):
        """
        Opens up a modal dialogue for picking difficulty
        """
        # animate the blur effect
        Animation(blur_amount=10, duration=0.3).start(self)
        difficulty_menu = DifficultyMenu(parent_screen=self)
        difficulty_menu.open()

    def select_level(self):
        """
        Triggered when an user selects a level
        """
        self.manager.init_transition(self.next_screen)

    def next_screen(self):
        """
        Transition to the next screen
        This function is called after the first animation plays
        and before the second animation plays
        """
        self.manager.switch_to(GameScreen())
