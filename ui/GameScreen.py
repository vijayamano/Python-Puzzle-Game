from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from levels.LevelHandler import LevelHandler
from ui.losemodal import LoseModal
from ui.cursorobject import CursorObject
from ui.menumodal import MenuModal
from ui.shapepicker import ShapePicker
from ui.colorpicker import ClayColorPicker
from ui.workspace import WorkSpace
from ui.levelshowbutton import LevelShowButton
from ui.leveltimer import LevelTimer
from ui.patternmodal import PatternModal
from kivy.animation import Animation
from ui.winmodal import WinnerModal
from audiohandler import AudioHandler
from kivy.properties import NumericProperty
from levels import (
    EASY_CLAY_LIMIT,
    EASY_TIME,
    EASY_VIEWS,
    HARD_CLAY_LIMIT,
    HARD_VIEWS,
    MEDIUM_CLAY_LIMIT,
    MEDIUM_TIME,
    HARD_TIME,
    MEDIUM_VIEWS,
)
from checker import Checker

Builder.load_file("ui/kv/gamescreen.kv")
Builder.load_file("ui/kv/clayjar.kv")


class ClayJar(ButtonBehavior, RelativeLayout):
    """
    This class is used to represent the clay jar. It controls the amount of
    clay inside the pot, if there is any more clay inside the pot. These
    parameters can be set and tweaked based on the level difficulty
    """

    current_clay_amount = NumericProperty(0)
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
        match self.cursor_object.pickup_clay(self.current_clay_amount):
            case 0:
                # we dropped the clay
                self.current_clay_amount += 1

            case 1:
                # we picked up the clay
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

    show_times = NumericProperty(0)
    """
    The number of times the level preview can be shown to the player
    """

    level_handler = None
    """
    The level handler object that is used to load the correct level or
    generate a new level
    """

    timer_running = False
    """
    Represents whether the timer is running or not
    """

    def __init__(self, level_handler, *args, **kwargs):
        self.level_handler = level_handler
        self.bg_texture = Image(
            source="assets/textures/start_bg.png", nocache=True
        ).texture
        self.bg_texture.uvsize = (1, 2)
        self.bg_texture.wrap = "repeat"
        self.name = "game_screen"
        # set show times based on difficulty
        if self.level_handler.current_difficulty == 0:
            self.show_times = EASY_VIEWS
        elif self.level_handler.current_difficulty == 1:
            self.show_times = MEDIUM_VIEWS
        else:
            self.show_times = HARD_VIEWS
        super().__init__(*args, **kwargs)
        # create a cursor object and add it to screen
        self.cursor_object = CursorObject()
        self.add_widget(self.cursor_object)
        # set the clay jar's cursor picker
        self.ids.clay_jar.cursor_object = self.cursor_object
        # assign the clay amount based on the difficulty
        if self.level_handler.current_difficulty == 0:
            self.ids.clay_jar.current_clay_amount = EASY_CLAY_LIMIT
        elif self.level_handler.current_difficulty == 1:
            self.ids.clay_jar.current_clay_amount = MEDIUM_CLAY_LIMIT
        else:
            self.ids.clay_jar.current_clay_amount = HARD_CLAY_LIMIT
        # set the shape picker cursor object
        self.ids.shape_picker.cursor_object = self.cursor_object
        # set the color picker cursor object
        self.ids.color_picker.cursor_object = self.cursor_object
        # set the shape picker reference of the color picker
        self.ids.color_picker.shape_picker = self.ids.shape_picker
        # set the workspace cursor object
        self.ids.workspace.cursor_object = self.cursor_object
        # bind the level show button to our function
        self.ids.level_show_button.bind(on_release=self.show_level)
        # if the main bgm is not playing we play it again
        AudioHandler().start_main_bgm()

    def on_enter(self, *args):
        self.show_level()
        return super().on_enter(*args)

    def show_level(self, *args):
        """
        Shows the modal view of the level preview and reduces the
        total number of previews available.
        """
        AudioHandler().click_sound()
        if self.show_times > 0:
            self.show_times -= 1
            self.ids.level_show_button.show_times = self.show_times
            pattern_modal = PatternModal(
                level_no=self.level_handler.current_level,
                preview_path=self.level_handler.get_preview_path(),
            )
            pattern_modal.bind(on_dismiss=self.start_level)
            pattern_modal.parent_screen = self
            pattern_modal.open()
        else:
            self.cursor_object.show_popup(
                "Out of Luck!", "You have no more previews left!"
            )

    def start_level(self, *args):
        """
        Starts the level and shows the timer. Also starts the timer
        """
        # play audio
        AudioHandler().click_sound()
        if not self.timer_running:
            if self.level_handler.current_difficulty == 0:
                duration = EASY_TIME
            elif self.level_handler.current_difficulty == 1:
                duration = MEDIUM_TIME
            else:
                duration = HARD_TIME
            self.ids.level_timer.start_timer(duration, self.on_timer_end)
            self.timer_running = True

    def button_start_level(self, modal, *args):
        """
        Starts the level and shows the timer. Also starts the timer
        """
        modal.dismiss()

    def on_timer_end(self, *args):
        """
        Called when the timer ends. Shows the game over popup
        """
        self.timer_running = False
        self.ids.level_timer.stop_timer()
        lostmenu = LoseModal(parent_screen=self)
        lostmenu.open()

    def submit(self, *args):
        AudioHandler().click_sound()
        self.ids.level_timer.stop_timer()
        self.ids.workspace.ids.container.export_to_png("assets/tmp/user_work.png")
        temp = Checker()
        factor = temp.check(
            "assets/tmp/user_work.png", self.level_handler.get_preview_path()
        )
        # If the AI produces a similarity factor of above 0.75 then the player has won
        if factor > 0.75:
            # play the win sound
            AudioHandler().win_sound()
            winmodal = WinnerModal(parent_screen=self)
            winmodal.open()
        else:
            # play the lose sound
            AudioHandler().lose_sound()
            losemodal = LoseModal(parent_screen=self)
            losemodal.open()

    def continue_level(self, modal, *args):
        """
        Called when the player presses the continue button on the win modal
        """
        # play auudio
        AudioHandler().click_sound()
        # close the modal
        modal.dismiss()
        self.manager.init_transition(self.move_to_next_level)

    def move_to_next_level(self, *args):
        """
        Moves the game to the next level
        """
        self.ids.level_timer.stop_timer()
        # first check if we are in the endless mode
        if self.level_handler.generated:
            # we are in endless mode so we need to generate the next level before transitioning
            self.level_handler.level_gen.clear_level()  # clear the level generator state
            self.level_handler.generate_level(self.level_handler.current_difficulty)
            self.manager.switch_to(GameScreen(self.level_handler))
            return
        # increment the current level handler current level by 1
        self.level_handler.current_level = str(
            int(self.level_handler.current_level) + 1
        )
        # check if there is any change in the difficulty
        if int(self.level_handler.current_level) <= 20:
            self.level_handler.current_difficulty = 0
        elif int(self.level_handler.current_level) <= 40:
            self.level_handler.current_difficulty = 1
        else:
            self.level_handler.current_difficulty = 2
        self.level_handler.generated = False
        self.manager.switch_to(GameScreen(self.level_handler))

    def main_menu(self, modal, *args):
        """
        Called when the player presses the main menu button on the win modal
        """
        # play audio
        AudioHandler().click_sound()
        self.ids.level_timer.stop_timer()
        # close the modal
        modal.dismiss()
        self.manager.init_transition(self.move_to_main_menu)

    def move_to_main_menu(self, *args):
        """
        Moves the game to the main menu
        """
        from ui.levelscreen import LevelScreen

        self.manager.switch_to(LevelScreen())

    def retry_level(self, modal, *args):
        """
        Called when the player presses the retry button on the lose modal
        """
        # play audio
        AudioHandler().click_sound()
        self.ids.level_timer.stop_timer()
        # close the modal
        modal.dismiss()
        self.manager.init_transition(self.move_to_retry_level)

    def move_to_retry_level(self, *args):
        """
        Resets the gamesceen
        """
        # first check if we are in the endless mode
        if self.level_handler.generated:
            # we are in endless mode
            self.manager.switch_to(GameScreen(self.level_handler))
            return
        self.level_handler.generated = False
        self.manager.switch_to(GameScreen(self.level_handler))

    def show_pause_menu(self, *args):
        """
        Shows the pause menu
        """
        # play audio
        AudioHandler().click_sound()
        MenuModal(parent_screen=self).open()
