from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty
from kivy.uix.image import Image
from kivy.effects.scroll import ScrollEffect
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from levels.levelhandler import LevelHandler
from ui.hoverbehaviour import HoverBehavior


Builder.load_string(
    """
<LevelScreen>:
    name: "level_screen"

    ScrollView:
        id: scroll_view
        size_hint:1,1
        pos_hint:{"center_x":0.5,"center_y":0.5}

        BoxLayout:
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
                    texture: root.bg_texture
            id: main_container
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
            padding: "90dp", "50dp", "90dp", "50dp"
            spacing: "50dp"
            pos_hint:{"center_x":0.5,"center_y":0.5}

            Image:          
                id: level_selector_title
                source: "assets/textures/level_selector_title.png"
                size_hint:None,None
                size: self.texture_size[0]*1.5,self.texture_size[1]*1.5
                pos_hint:{"center_x":0.5,"center_y":0.5}

            GridLayout:
                id: level_selector_grid
                cols: 3
                size_hint_y: None
                height: self.minimum_height
                spacing: "90dp"
                

<LevelCard>:
    size_hint: 1, None
    height: self.width
    orientation: "vertical"
    padding: "10dp", "20dp", "10dp", "10dp"
    canvas.before:
        Color:
            rgba: 0, 0, 0, 0.85
        BoxShadow:
            pos: self.pos
            size: self.size
            offset: 0, -5
            spread_radius: -10, -10
            border_radius: 10, 10, 10, 10
            blur_radius: 40 if not self.hovering else 80

        Color:
            rgba: 1,1,1,1
        Rectangle:
            size: self.size if not self.hovering else self.container_size
            pos: self.pos if not self.hovering else (self.center[0] - self.container_size[0] / 2, self.center[1] - self.container_size[1] / 2)
            source: "assets/textures/level_card.png"

    AnchorLayout:
        size_hint: 1,.7
        anchor_x: "center"
        anchor_y: "center"
        Image:
            id:level_card_bg
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
        padding: "10dp", "0dp", "10dp", "0dp"

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
                allow_stretch: True

            Label:
                id:level_card_title
                text: "Level "+str(root.level_no)
                font_size: "30dp"
                color: 1,1,1,1
                font_name: "assets/fonts/main.ttf"

"""
)


class LevelCard(BoxLayout, HoverBehavior):
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

    level_no = None
    """
    The level number
    """

    preview_path = None
    """
    The path to the preview image
    """

    difficulty = None
    """
    The difficulty of the level
    """

    difficulty_image = None

    def __init__(self, level_no, preview_path, difficulty, *args, **kwargs):
        self.level_no = level_no
        self.preview_path = preview_path
        self.difficulty = difficulty
        if self.difficulty == "easy":
            self.difficulty_image = "assets/textures/difficulty.png"
        elif self.difficulty == "medium":
            self.difficulty_image = "assets/textures/difficulty-1.png"
        elif self.difficulty == "hard":
            self.difficulty_image = "assets/textures/difficulty-2.png"
        super().__init__(*args, **kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_enter(self, *args):
        """
        triggers when the mouse enters the widget
        """
        self.container_size = self.size
        self.hovering = True
        Animation(
            container_size=(self.size[0] + 20, self.size[1] + 20), duration=0.2
        ).start(self)

    def on_leave(self, *args):
        """
        triggers when the mouse leaves the widget
        """
        anim = Animation(
            container_size=(self.size[0], self.size[1]),
            duration=0.2,
        )
        anim.bind(on_complete=self.set_false)
        anim.start(self)

    def set_false(self, *args):
        self.hovering = False


class LevelScreen(Screen):
    """
    This is the screen that shows the level select screen.
    """

    bg_texture = ObjectProperty(None)

    level_handler = LevelHandler()

    def __init__(self, *args, **Kwargs):
        super().__init__(*args, **Kwargs)
        self.bg_texture = Image(source="assets/textures/start_bg.png").texture
        self.bg_texture.wrap = "repeat"
        self.bg_texture.uvsize = (1, 10)
        # cancel the scroll effect
        self.ids.scroll_view.effect_cls = ScrollEffect
        # Load the level cards
        self.load_levels()

    def on_start():
        pass

    def load_levels(self):
        """ "
        Loads the levels from the level generator.
        """
        self.level_handler.load_levels()
        count = 0
        # add the easy levels to the grid
        for level in self.level_handler.easy_levels:
            count += 1
            self.ids.level_selector_grid.add_widget(
                LevelCard(count, level.preview_path, level.difficulty)
            )
        # add the medium levels to the grid
        for level in self.level_handler.medium_levels:
            count += 1
            self.ids.level_selector_grid.add_widget(
                LevelCard(count, level.preview_path, level.difficulty)
            )
        # add the hard levels to the grid
        for level in self.level_handler.hard_levels:
            count += 1
            self.ids.level_selector_grid.add_widget(
                LevelCard(count, level.preview_path, level.difficulty)
            )
